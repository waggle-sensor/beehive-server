#!/usr/bin/env python
import web
import os.path
import subprocess
import threading
import re
import MySQLdb
import logging


logger = logging.getLogger(__name__)

port = 80

resource_lock = threading.RLock()

script_path = "/usr/lib/waggle/beehive-server/SSL/"
ssl_path = "/usr/lib/waggle/SSL/"
ssl_path_nodes = ssl_path+"nodes/"


hexaPattern = re.compile(r'^([0-9A-F]*)$')
prog = re.compile(hexaPattern)

authorized_keys_file = ssl_path_nodes+"authorized_keys"


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
        
        if nodeid:
            
            # check for 16 digit hex
            if len(nodeid) != 16:
                print "node_id has wrong length."
                return "node_id not recognized"
                
            try:
                int(nodeid, 16)
            except ValueError:
                print "node_id not hex."
                return "node_id not recognized"
                
            
            print "Using nodeid: "+str(nodeid)
            node_dir = ssl_path_nodes + 'node_'+ nodeid
            if not os.path.isdir(node_dir):
                with resource_lock:
                    subprocess.call([script_path + 'create_client_cert.sh', 'node', 'nodes/node_'+ nodeid])
                    time.sleep(1)
                    append_command = "cat {0}node_{1}/key_rsa.pub >> {2}".format(ssl_path_nodes, nodeid, authorized_keys_file)
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
        else:
            print "No node_id provided."
            return "No node_id provided."
            #with resource_lock:
            #    subprocess.call([script_path + 'create_client_cert.sh', 'node', 'temp_client_cert'])
            #    privkey = read_file(ssl_path + 'temp_client_cert/key.pem')
            #    cert    = read_file(ssl_path + 'temp_client_cert/cert.pem')
            
        if not privkey:
            return "error: privkey file not found !?"
        
        if not cert:
            return "error: cert file not found !?"

        if nodeid:
            print "issuing cert for node "+nodeid
        else:
            print "issuing cert for unknown node"
        return privkey + "\n" + cert


def mysql_query_generator(query):
    db = MySQLdb.connect(host="beehive-mysql",    
                         user="waggle",       
                         passwd="waggle",  
                         db="waggle")      

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    logger.debug("query: " + query)
    cur.execute(query)


    # get array:
    for row in cur.fetchall():
        yield row

    db.close()


def find_port(node_id):
    for row in mysql_query_generator("SELECT reverse_ssh_port FROM nodes WHERE node_id='{0}'".format(node_id)):
        
        try:
            port = int(row[0])
        except ValueError:
            logger.error("Could not parse port number %s" % (port)) 
            port = None  
        
        
        return port
    return None

if __name__ == "__main__":
    
    
    # get port: for node_id SELECT reverse_ssh_port FROM nodes WHERE node_id='0000001e06200335';
    
    for row in mysql_query_generator("SELECT * FROM nodes"):
        print row
    
    # get all ports:
    for row in mysql_query_generator("SELECT node_id,reverse_ssh_port FROM nodes"):
        print row
    
    port = find_port('0000001e06200335')
    print "port: ", port
    
    
    # create new authorized_keys file on every start, just to be sure.
    
    merge_command = "cat {0}node_*/key_rsa.pub > {1}".format(ssl_path_nodes, authorized_keys_file)
    logger.debug("command: "+ merge_command)
    # manual recreaetion of authorized_keys file: 
    # cat node_*/key_rsa.pub > authorized_keys 
    subprocess.call(merge_command, shell=True)
    
    chmod_cmd = "chmod 600 {0}".format(authorized_keys_file)
    logger.debug ( "command: "+ chmod_cmd)
    subprocess.call(chmod_cmd, shell=True)
    
    logger.debug( "create "+authorized_keys_file)
    
    
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))
    app.run()




