#!/usr/bin/env python3
import argparse
from binascii import unhexlify
import datetime
import json
import logging
import os
import pika
import re
import subprocess
import sys
import time

global verbosity

""" Registers a new virtual node on a beehive.
    Creates a directory with all the files that comprise a soft-node / virtual node.
    The contents of this directory are all that is necessary to transmit data to the beehive.
    
    USAGE:
        soft-node-register.py  <beehive-url>  <node_id>  <dir>  <registration_key_path>
    eg.
        soft-node-register.py  10.10.10.183   000002000000ffff  /home/wcatino/node0  /home/wcatino/aot_waggle_id_rsa_registration
    NOTE: This must be run from the root account on the client (not necessarily on the server).
    This code was adapted from the nodecontroller code that registers a node with a beehive.
"""

# pika - let's make it verbose...
logging.getLogger('pika').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.WARNING)

#_______________________________________________________________________
# Run a command, return its output as a single string
def CmdString(command):
    print('cmd = ', command)
    return subprocess.getoutput(command)

#_______________________________________________________________________
# Run a command, return the output as a list of strings
def CmdList(command, bDebug = True):
    strResult = subprocess.getoutput(command)
    if bDebug:
        print('CmdList:   command = ', command,'\n   strResult = ', strResult)
    if len(strResult):
        result = strResult.split('\n')
    else:
        result = []
    return result

#_______________________________________________________________________
# Run a command and capture it's output
def Cmd0(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    return iter(p.stdout.readline, b'')

#_______________________________________________________________________
# Run a command and capture it's output - return iterable like result of open()
def Cmd1(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  shell = True,
                                  universal_newlines = True)
    #return iter(p.stdout.readline, b'')
    return p.stdout
 
#_______________________________________________________________________
def GetPortFromNode(nodeId):
    nodeId = nodeId.lower()
    dictNodeToPort = GetDictNodeToPort()
    port = None
    if nodeId in dictNodeToPort:
        port = dictNodeToPort[nodeId]
    return port

    
#_______________________________________________________________________
def DatetimeFromString(strTime):
    if len(strTime) == 19:
        result = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")
    else:
        result = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S.%f")
    return result
#_______________________________________________________________________
def DatetimeToString(t):
    return t.strftime("%Y-%m-%d %H:%M:%S.%f")
#_______________________________________________________________________
def DatetimeToDateString(t):
    return t.strftime("%Y-%m-%d")

    
    
#_______________________________________________________________________
# adapted from nodecontroller/registration-service
#_______________________________________________________________________
def run_registration_command(registration_key, cert_server, command):
  ssh_command =\
    ["ssh", cert_server,
     "-p", "20022",
     "-i", registration_key,
     "-o", "StrictHostKeyChecking no",
     command]
  logging.debug("Executing: {}".format(ssh_command))
  p = subprocess.Popen(
    ssh_command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
  return p.stdout.read().decode()

#_______________________________________________________________________
# adapted from nodecontroller/registration-service
#_______________________________________________________________________
def read_file( str ):
    print("read_file: "+str)
    if not os.path.isfile(str) :
        return ""
    with open(str,'r') as file_:
        return file_.read().strip()
    return ""



#_______________________________________________________________________
# adapted from nodecontroller/registration-service
#_______________________________________________________________________
def create_dir_for_file(file):
    file_dir = os.path.dirname(file)
    logging.debug("create_dir_for_file: {}".format(file_dir))
    if not os.path.exists(file_dir):
        try:
            os.makedirs(file_dir)
        except Exception as e:
            logging.error("Could not create directory '%s' : %s" % (file_dir,str(e)) )
            sys.exit(1)


#_______________________________________________________________________
# adapted from nodecontroller/registration-service
#_______________________________________________________________________
def get_certificates(dir):
    cert_server = ""
    #with open("/etc/waggle/server_host") as cert_server_file:
    with open(dir + "/server_host") as cert_server_file:
        cert_server = cert_server_file.readline().rstrip()
    node_id = ""
    #with open("/etc/waggle/node_id") as node_id_file:
    with open(dir + "/node_id") as node_id_file:
        node_id = node_id_file.readline().rstrip()
        
    #registration_key = "/root/id_rsa_waggle_aot_registration"
    registration_key =  dir + "/id_rsa_waggle_aot_registration"
    
    #reverse_ssh_port_file = '/etc/waggle/reverse_ssh_port'
    reverse_ssh_port_file = dir + '/reverse_ssh_port'
    
    #ca_root_file = "/usr/lib/waggle/SSL/waggleca/cacert.pem"
    ca_root_file = dir + "/cacert.pem"
    
    #client_key_file = "/usr/lib/waggle/SSL/node/key.pem"
    client_key_file = dir + "/node/key.pem"
    
    #client_cert_file = "/usr/lib/waggle/SSL/node/cert.pem"
    client_cert_file = dir + "/node/cert.pem"

    loop=-1
    while True:
        loop=(loop+1)%20
        ca_root_file_exists = os.path.isfile(ca_root_file) and os.stat(ca_root_file).st_size > 0
        client_key_file_exists = os.path.isfile(client_key_file) and os.stat(client_key_file).st_size > 0
        client_cert_file_exists = os.path.isfile(client_cert_file) and os.stat(client_cert_file).st_size > 0
        reverse_ssh_port_file_exists = os.path.isfile(reverse_ssh_port_file) and os.stat(reverse_ssh_port_file).st_size > 0

        #check if cert server is available
        if not (ca_root_file_exists and client_key_file_exists and client_cert_file_exists and reverse_ssh_port_file_exists):

            if not (os.path.isfile(registration_key) and os.stat(registration_key).st_size > 0):
                logging.error("Registration file '{}' not found.".format(registration_key))
        
            if (loop == 0):
                if not ca_root_file_exists:
                    logging.info("File '%s' not found." % (ca_root_file))
                if not client_key_file_exists:
                    logging.info("File '%s' not found." % (client_key_file))
                if not client_cert_file_exists:
                    logging.info("File '%s' not found." % (client_cert_file))
                if not reverse_ssh_port_file_exists:
                    logging.info("File '%s' not found." % (reverse_ssh_port_file))

            try:
                html = run_registration_command(registration_key, cert_server, "")
            except Exception as e:
                if (loop == 0):
                    logging.error('Have not found certificate files and can not connect to certificate server (%s): %s' % (cert_server, str(e)))
                    logging.error('Either copy certificate files manually or activate certificate sever.')
                    logging.error('Will silently try to connect to certificate server in 30 second intervals from now on.')

                time.sleep(30)
                continue

            if html != 'This is the Waggle certificate server.':
                if (loop == 0):
                    logging.error(''.join(("Unexpected response from certificate server: ", html)))
                time.sleep(5)
                continue
        else:
            logging.info("All certificate files found.")
            if os.path.isfile(registration_key):
                os.remove(registration_key)
            break

        # make sure certficate files exist.
        if not ca_root_file_exists:
            create_dir_for_file(ca_root_file)
            logging.info("trying to get server certificate from certificate server %s..." % (cert_server))
            try:
                html = run_registration_command(registration_key, cert_server, "certca")
            except Exception as e:
                logging.error('Could not connect to certificate server: '+str(e))
                time.sleep(5)
                continue

            if html.startswith( '-----BEGIN CERTIFICATE-----' ) and html.endswith('-----END CERTIFICATE-----'):
                logging.info('certificate downloaded')
            else:
                logging.error('certificate parsing problem')
                if logging.isEnabledFor(logging.DEBUG):
                    logging.debug('content: '+str(html))
                time.sleep(5)
                continue

            with open(ca_root_file, 'w') as f:
                f.write(html)
            f.close()

            logging.debug("File %s written." % (ca_root_file))

        if not (client_key_file_exists and client_cert_file_exists):
            create_dir_for_file(client_key_file)
            create_dir_for_file(client_cert_file)
            logging.info("trying to get node key and certificate from certificate server %s..." % (cert_server))
            try:
                html = run_registration_command(registration_key, cert_server, "node?%s" % node_id)
            except Exception as e:
                logging.error('Could not connect to certificate server: '+str(e))
                if logging.isEnabledFor(logging.DEBUG):
                    logging.debug('content: '+str(html))
                time.sleep(5)
                continue
            if 'error: cert file not found' in html:
              raise Exception(''.join(('Node ID ', node_id, ' is already registered but the associated SSL credentials were not found.')))

            priv_key_start = "-----BEGIN RSA PRIVATE KEY-----"
            position_rsa_priv_key_start = html.find(priv_key_start)
            if position_rsa_priv_key_start == -1:
                logging.error("Could not parse PEM data from server. (position_rsa_priv_key_start)")
                time.sleep(5)
                continue
            logging.info("position_rsa_priv_key_start: "+str(position_rsa_priv_key_start))

            priv_key_end = "-----END RSA PRIVATE KEY-----"
            position_rsa_priv_key_end = html.find(priv_key_end)
            if position_rsa_priv_key_end == -1:
                logging.error("Could not parse PEM data from server. (position_rsa_priv_key_end)")
                time.sleep(5)
                continue
            logging.info("position_rsa_priv_key_end: "+str(position_rsa_priv_key_end))

            position_cert_start = html.find("-----BEGIN CERTIFICATE-----")
            if position_cert_start == -1:
                logging.error("Could not parse PEM data from server. (position_cert_start)")
                time.sleep(5)
                continue
            logging.info("position_cert_start: "+str(position_cert_start))

            end_cert = "-----END CERTIFICATE-----"
            position_cert_end = html.find(end_cert)
            if position_cert_end == -1:
                logging.error("Could not parse PEM data from server. (position_cert_end)")
                time.sleep(5)
                continue
            logging.info("position_cert_end: "+str(position_cert_end))

            html_tail = html[position_cert_end+len(end_cert):]

            client_key_string = html[position_rsa_priv_key_start:position_rsa_priv_key_end+len(priv_key_end)]+"\n"
            client_cert_string = html[position_cert_start:position_cert_end+len(end_cert)]+"\n"


            # find port for reverse ssh tunnel
            port_number = re.findall("PORT=(\d+)", html_tail)[0]

            rsa_public_key, rsa_public_key_comment = re.findall("(ssh-rsa \S*)( .*)?", html_tail)[0]

            logging.debug("client_key_file: "+client_key_string)
            logging.debug("client_cert_file: "+client_cert_string)

            logging.debug("PORT: "+str(port_number))


            # write everything to files
            with open(client_key_file, 'w') as f:
                f.write(client_key_string)
            f.close()
            logging.info("File '%s' has been written." % (client_key_file))
            if False:
                subprocess.call(['chown', 'rabbitmq:rabbitmq', client_key_file])
            else:
                print('skipping chown!!!!!!!!!!!!!!')
            os.chmod(client_key_file, 0o600)

            with open(client_cert_file, 'w') as f:
                f.write(client_cert_string)
            f.close()
            if False:
                subprocess.call(['chown', 'rabbitmq:rabbitmq', client_cert_file])
            else:
                print('skipping chown!!!!!!!!!!!!!!')

            os.chmod(client_cert_file, 0o600)

            logging.info("File '%s' has been written." % (client_cert_file))

            with open(reverse_ssh_port_file, 'w') as f:
                f.write(str(port_number))
            f.close()

            logging.info("File '%s' has been written." % (reverse_ssh_port_file))

        
#_______________________________________________________________________
#_______________________________________________________________________
if __name__ == '__main__':
    global verbosity
    
    # get args
    argParser = argparse.ArgumentParser()
    argParser.add_argument('beehive_url', help = 'url of the beehive to connect')
    argParser.add_argument('node_id', help = 'id of node, eg. 000002000000ffff')
    argParser.add_argument('dir', help = 'directory for storing id files and credentials')
    argParser.add_argument('registration_key_path', help = 'path to registration_key file')
    argParser.add_argument('--verbose', '-v', action='count', default=0)
    args = argParser.parse_args()
    
    verbosity = args.verbose
    beehive_url = args.beehive_url
    node_id = args.node_id
    dir = args.dir
    registration_key_path = args.registration_key_path
    
    if verbosity > 2:   logging.basicConfig(level=logging.DEBUG)
    elif verbosity > 1: logging.basicConfig(level=logging.INFO)
    else:               logging.basicConfig(level=logging.WARNING)
    
    logging.debug('args = ', args)
    
    # node_id must be of the form (without spaces)
    #    00 00 02 00 00 00 xx xx
    bValidNodeId = False
    if node_id and len(node_id) == 16:
        node_id = node_id.lower()
        if re.match('^000002000000[0-9a-f]{4}$', node_id):
            print('VALID node_id = {}'.format(node_id))
            bValidNodeId = True
    if not bValidNodeId:
        print('INVALID node_id = {}'.format(node_id))
        sys.exit()
    
    # create directory
    CmdString('mkdir -p {}'.format(dir))
    
    # copy registration key
    CmdString('cp {} {}/id_rsa_waggle_aot_registration'.format(registration_key_path, dir))
    CmdString('chmod 600 {}/id_rsa_waggle_aot_registration'.format(dir))

    # create server host file
    with open(dir + "/server_host", 'w') as cert_server_file:
        cert_server_file.write(beehive_url + '\n')
        
    # create node_id file
    with open(dir + "/node_id", 'w') as node_id_file:
        node_id_file.write(node_id + '\n')
   
    # get all the necessary certificate files, etc.
    get_certificates(dir)
   
    print('Registration complete.')
    
    
    
    
    