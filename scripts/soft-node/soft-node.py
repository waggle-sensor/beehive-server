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


""" Stream data to a beehive just like a node.

    ./soft-node.py  <dir>  <data_file>

"""

# pika - let's make it verbose...
logging.getLogger('pika').setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING)

#_______________________________________________________________________
# Run a command, return its output as a single string
def CmdString(command):
    print('cmd = ', command)
    return subprocess.getoutput(command)

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
#_______________________________________________________________________
def DataSerialize(data):
    if isinstance(data, int):
        content_type = 'i'
        body = str(data).encode()
    elif isinstance(data, float):
        content_type = 'f'
        body = str(data).encode()
    elif isinstance(data, str):
        content_type = 's'
        body = data.encode()
    elif isinstance(data, bytearray):
        content_type = 'b'
        body = bytes(data)
    elif isinstance(data, bytes):
        content_type = 'b'
        body = data
    elif isinstance(data, dict) or isinstance(data, list):
        content_type = 'j'
        body = json.dumps(data).encode()
    else:
        raise ValueError('unsupported data type')

    return content_type, body
    
#_______________________________________________________________________
#_______________________________________________________________________
if __name__ == '__main__':

    # get args
    argParser = argparse.ArgumentParser(description='Sends all the data in <data_file> to the beehive as a node, with parameters specified in <dir>.')
    argParser.add_argument('dir', help = 'directory containing id files and credentials')
    argParser.add_argument('data_file', help = """path of file that contains data to transmit.  Each line contains the timestamp in ms since epoch, followed by whitespace, followed by hexlify'ed binary data, followed by linebreak.""")
    argParser.add_argument('--verbose', '-v', action='count', default=0)
    argParser.add_argument('-testMessage', action='store')
    args = argParser.parse_args()
    
    dir = args.dir
    data_file = args.data_file
    
    if args.verbose > 2:    logging.basicConfig(level=logging.DEBUG)
    elif args.verbose > 1:  logging.basicConfig(level=logging.INFO)
    else:                   logging.basicConfig(level=logging.WARNING)

    logging.debug('args = ' + str(args))
    
    # store file paths in variables
    server_host_file        = dir + "/server_host"
    node_id_file            = dir + "/node_id"
    reverse_ssh_port_file   = dir + '/reverse_ssh_port'
    ca_root_file            = dir + "/cacert.pem"
    client_key_file         = dir + "/node/key.pem"
    client_cert_file        = dir + "/node/cert.pem"

    # check if directory exists
    if not os.path.isdir(dir):
        logging.error('ERROR: Directory does not exist: {}'.format(dir))
        sys.exit(-1)
    else:
        logging.debug('Found dir: {}'.format(dir))
        
    # check for all the necessary files
    for fn in [server_host_file, 
                ca_root_file, 
                client_key_file, 
                client_cert_file]:
        logging.debug('...testing file: {}'.format(fn))
        if not os.path.isfile(fn):
            logging.error('Missing file: {}'.format(fn))
            sys.exit(-1)
        elif  not (os.stat(fn).st_size > 0):
            logging.error('Size 0 file : {}'.format(fn))
            sys.exit(-1)
            
    # load server_host
    with open(server_host_file, 'r') as f:
        server_host = f.readline().strip()
        logging.info('server_host = {}'.format(server_host))

    # load node_id
    with open(node_id_file, 'r') as f:
        node_id = f.readline().strip().lower()
        logging.info('node_id = {}'.format(node_id))
        
        # soft/virtual node node_id must be of the form (without spaces)
        #    00 00 02 00 00 00 xx xx
        bValidNodeId = False
        if node_id and len(node_id) == 16:
            if re.match('^000002000000[0-9a-f]{4}$', node_id):
                print('VALID node_id = {}'.format(node_id))
                bValidNodeId = True
                
        if not bValidNodeId:
            print('INVALID node_id = {}'.format(node_id))
            sys.exit(-1)
    
    # open a connection
    # URI:    amqps://node:waggle@beehive1.mcs.anl.gov:23181?cacertfile=/usr/lib/waggle/SSL/waggleca/cacert.pem&certfile=/usr/lib/waggle/SSL/node/cert.pem&keyfile=/usr/lib/waggle/SSL/node/key.pem&verify=verify_peer"
    
    credentials = pika.credentials.PlainCredentials('node', 'waggle')
    
    ssl_options={'ca_certs' : dir + "/cacert.pem",
                'certfile'  : dir + "/node/cert.pem",
                'keyfile'   : dir + "/node/key.pem"}
    logging.debug('ssl_options = ', ssl_options)
    
    params = pika.ConnectionParameters(
                    host=server_host, 
                    port=23181, 
                    credentials=credentials, 
                    ssl=True, 
                    ssl_options=ssl_options,
                    retry_delay=10,
                    socket_timeout=10)
    logging.debug('params = {}'.format(params))
    
    connection = pika.BlockingConnection(params)
    logging.debug('connection = {}'.format(connection))
    
    channel = connection.channel()
    logging.debug('channel = {}'.format(channel))
    
    iLine=0
    if (args.testMessage):   # test message
        properties = pika.BasicProperties(
                    headers = {
                        'value' : 80, 
                        'reply_to' : node_id},
                    timestamp=int(time.time()),
                    reply_to=node_id)
        logging.debug('properties = {}'.format(properties))
        
        channel.basic_publish(exchange='logs', 
                        routing_key='', 
                        body=args.testMessage, 
                        properties=properties)
        
    else:   # coresense data in a file
        # TODO get it from a file
        with open(data_file, 'r') as f:
            for iLine, line in enumerate(f):
                cols = line.split()
                if len(cols) < 2:
                    logging.warning('WARNING: Line {} contained less than 2 columnns'.format(iLine))
                else:
                    # headers = {'node_id' : node_id}
                    theTimestamp = int(cols[0])
                    data = unhexlify(cols[1])

                    content_type, body = DataSerialize(data)
                    logging.debug('content_type = {}'.format(content_type))
                    logging.debug('body = {}'.format(body))

                    properties = pika.BasicProperties(
                            reply_to=node_id,   # node_id goes here
                            #headers=headers,
                            delivery_mode=2,
                            timestamp=theTimestamp,    # int(time.time() * 1000),
                            content_type=content_type,
                            type='frame', #sensor,  for raw coresense data, it's "frame"
                            app_id='coresense:3')   # plugin id goes here too

                    channel.basic_publish(
                            properties=properties,
                            exchange='data-pipeline-in',
                            routing_key=properties.app_id,  # plugin id goes here too
                            body=body)
    
    logging.info('Communication complete.  [# of lines: {}]'.format(iLine))

    