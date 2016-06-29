#!/usr/bin/env python
import web
import os.path
import subprocess
import threading
import re
import sys
import logging
import pprint
import time
from os import listdir
from os.path import isdir, join
sys.path.append("..")
from waggle_protocol.utilities.mysql import *


LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - line=%(lineno)d - %(message)s'
formatter = logging.Formatter(LOG_FORMAT)
loglevel = logging.DEBUG

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)

logger.addHandler(handler)
logger.setLevel(loglevel)

root_logger = logging.getLogger()
root_logger.setLevel(loglevel)




httpserver_port = 80

resource_lock = threading.RLock()

script_path = "/usr/lib/waggle/beehive-server/SSL/"
ssl_path = "/usr/lib/waggle/SSL/"
ssl_path_nodes = ssl_path+"nodes/"


hexaPattern = re.compile(r'^([0-9A-F]*)$')
prog = re.compile(hexaPattern)

authorized_keys_file = ssl_path_nodes+"authorized_keys"

db = None

def read_file( str ):
    print "read_file: "+str
    if not os.path.isfile(str) :
        return ""
    with open(str,'r') as file_:
        return file_.read().strip()
    return ""





urls = (
    '/certca', 'certca',
    '/node/?', 'newnode',
    '/', 'index'
)

app = web.application(urls, globals())

class index:        
    def GET(self):
        return 'This is the Waggle certificate server.'

class certca:        
    def GET(self):
        result = read_file(ssl_path + "waggleca/cacert.pem")
        if not result:
            return "error: cacert file not found !?"

        return result

class newnode:        
    def GET(self):
        
        
        query = referer = web.ctx.query
        nodeid=None
        
        print "query: "+str(query)
        
        global prog
        # TODO: make it an option to allow or disallow anonymous nodes
        if len(query) > 1 :
            
            if query.startswith("?"):
                nodeid = query[1:].upper()
                
                result = prog.match(nodeid)
                if not result:
                    return "error: Could not parse node id."
                    
                # TODO check that this is a valid node id
            else:
                return "error: Could not parse query. Questionmark missing."
        else:
            print "requested cert without nodeid"
        
        
        privkey=""
        cert=""
        
        if not nodeid:
            print "No node_id provided."
            return "No node_id provided."
            
            
        # check for 16 digit hex
        if len(nodeid) != 16:
            print "node_id has wrong length."
            return "node_id not recognized"
            
        try:
            int(nodeid, 16)
        except ValueError:
            print "node_id not hex."
            return "node_id not recognized"
        
        key_rsa_pub_file = "{0}node_{1}/key_rsa.pub".format(ssl_path_nodes, nodeid)
            
        ##### Got node_id #####
        print "Using nodeid: "+str(nodeid)
        node_dir = ssl_path_nodes + 'node_'+ nodeid
        if not os.path.isdir(node_dir):
            with resource_lock:
                subprocess.call([script_path + 'create_client_cert.sh', 'node', 'nodes/node_'+ nodeid])
                time.sleep(1)
                append_command = "cat {0} >> {1}".format(key_rsa_pub_file, authorized_keys_file)
                print "command: ", append_command
                # manual recreaetion of authorized_keys file: 
                # cat node_*/key_rsa.pub > authorized_keys 
                subprocess.call(append_command, shell=True)
                
                chmod_cmd = "chmod 600 {0}".format(authorized_keys_file)
                print "command: ", chmod_cmd
                subprocess.call(chmod_cmd, shell=True)
                # manual recreation of authorized_keys file: 
                # cat node_*/key_rsa.pub > authorized_keys
        
        
        privkey = read_file(node_dir + '/key.pem')
        cert    = read_file(node_dir + '/cert.pem')
        
        key_rsa_pub_file_content  = read_file(key_rsa_pub_file)
        
        
        db = Mysql( host="beehive-mysql",    
                        user="waggle",       
                        passwd="waggle",  
                        db="waggle")
        #logger.warning("should not happen")
        
        
        mysql_row_node = db.get_node(nodeid)
        
        if not mysql_row_node:
            port=db.createNewNode(nodeid)
            if not port:
                print "Error: Node creation failed"
                return "Error: Node creation failed"
            mysql_row_node = db.get_node(nodeid)
        
        
        
        #port = mysql_row_node[4]
        port = db.find_port(nodeid)
        
        if not port:
            print "Error: Node creation failed, port not found"
            return "Error: Node creation failed, port not found"
        
        try:
            port = int(port)
        except:
            print "Error: Node creation failed, port is not an int"
            return "Error: Node creation failed, port is not an int"
            
        
        if port:
            logger.debug("port number found: %d" % (port))
        else:
            logger.debug("Error: port number not found !?")
            return "Error: port number not found !?"
            
        
            
        if not privkey:
            return "error: privkey file not found !?"
        
        if not cert:
            return "error: cert file not found !?"

        if nodeid:
            print "issuing cert for node "+nodeid
        else:
            print "issuing cert for unknown node"
        return privkey + "\n" + cert + "\nPORT="+str(port) + "\n" + key_rsa_pub_file_content + "\n"





if __name__ == "__main__":
    
    
    node_database={}

    # get all public keys from disk
    for d in listdir(ssl_path_nodes):
        if isdir(join(ssl_path_nodes, d)) and d[0:5] == 'node_':
            rsa_pub_filename =  ssl_path_nodes+'/'+d+'/key_rsa.pub'
            try:
                with open(rsa_pub_filename, 'r') as rsa_pub_file:
                    data=rsa_pub_file.read()
                    node_id = d[5:].upper()
                    node_database[node_id] = {}
                    node_database[node_id]['pub']=data
            except Exception as e:
                logger.error("Error reading file %s: %s" % (rsa_pub_filename, str(e)))
            


    print str(node_database)
    
    
    
    db = Mysql( host="beehive-mysql",    
                user="waggle",       
                passwd="waggle",  
                db="waggle")
    
    # get port: for node_id SELECT reverse_ssh_port FROM nodes WHERE node_id='0000001e06200335';
    
    
    
    # get all ports:
    
    
    for row in db.query_all("SELECT * FROM nodes"):
        print row
    
    # get nodes and ports from database
    for row in db.query_all("SELECT node_id,reverse_ssh_port FROM nodes"):
        print row
        
        node_id = row[0].upper()
        
        if not node_id in node_database:
            logger.warning("Node %s is in database, but no public key was found")
            node_database[node_id] = {}
            
        
        port = int(row[1])
        if port:
            node_database[node_id]['reverse_ssh_port']=port
        else:
            logger.warning("node %s has no port assigned" % (node_id))
    
    # explicit check for consistency
    for node_id in node_database:
        #logger.debug("node_id: %s" % (node_id))
        if not 'reverse_ssh_port' in node_database[node_id]:
            logger.warning("Node %s has public key, but no port number is assigned in database." % (node_id))
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(node_database)
    
    auth_options = 'no-X11-forwarding,no-agent-forwarding,no-pty'
    new_authorized_keys_content = []
    for node_id in node_database.keys():
        line=None
        if 'reverse_ssh_port' in node_database[node_id]:
            port = node_database[node_id]['reverse_ssh_port']
            permitopen = 'permitopen="localhost:%d"' % (port)
            line="%s,%s %s" % (permitopen, auth_options, node_database[node_id]['pub'])
        else:
            # add public keys without port number, but comment the line
            if 'pub' in node_database[node_id]:
                permitopen = 'permitopen="localhost:?"'
                line="#%s,%s %s" % (permitopen, auth_options, node_database[node_id]['pub'])
        if line:
            logger.debug(line)
            new_authorized_keys_content.append(line)
            
    
    # create new authorized_keys file on every start, just to be sure.
    with open(authorized_keys_file, 'w') as file:
        for line in new_authorized_keys_content:
            file.write("%s\n" % line)
    
    chmod_cmd = "chmod 600 {0}".format(authorized_keys_file)
    logger.debug ( "command: "+ chmod_cmd)
    subprocess.call(chmod_cmd, shell=True)
    
    logger.debug( "create "+authorized_keys_file)
    
    
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", httpserver_port))
    app.run()




