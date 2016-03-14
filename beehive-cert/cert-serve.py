#!/usr/bin/env python
import web
import os.path
import subprocess
import threading
import re
import MySQLdb
import logging
import pprint
from os import listdir
from os.path import isdir, join
from contextlib import contextmanager


LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - line=%(lineno)d - %(message)s'

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

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
            
            port = find_port(nodeid)
            if port:
                logger.debug("port number found: %d" % (port))
            else:
                logger.debug("port number not found. Issue new one.")
            
                port = createNewNode(node_id)
            
            
            
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
        return privkey + "\n" + cert + "\nPORT="+port + "\n"


class Mysql(object):

    
    
    def __init__(self, host='localhost', user='', passwd='', db=''):

        self._host=host
        self._user=user
        self._passwd=passwd
        self._db=db
        


    @contextmanager
    def get_cursor(self, query):


        # using with does not work here
        db = MySQLdb.connect(  host=self._host,    
                                     user=self._user,       
                                     passwd=self._passwd,  
                                     db=self._db)
        cur = db.cursor()
        logger.debug("query: " + query)
        try:
            cur.execute(query)
            db.commit()
            logger.debug("query was successful")
        except Exception as e:
            logger.error("query failed: (%s) %s" % (str(type(e)), str(e) ) )
        
        yield cur
        
        cur.close()
        db.close()
        


    def query_all(self, query):
        """
        MySQL query that returns multiple results in form of a generator
        """
        with self.get_cursor(query) as cur:
            # get array:
            for row in cur.fetchall():
                yield row
                

    def query_one(self, query):
        """
        MySQL query that returns a single result
        """
        
        with self.get_cursor(query) as cur:
            return cur.fetchone()
        
        


    def find_port(self, node_id):
        row = self.query_one("SELECT reverse_ssh_port FROM nodes WHERE node_id='{0}'".format(node_id))
        
        if not row:
            return None
        
        try:
            port = int(row[0])
        except ValueError:
            logger.error("Could not parse port number %s" % (port)) 
            port = None  
    
        
            return port
        return None


    def createNewNode(self, node_id, description, port):
    #0000001e06200335
        self.query_one("INSERT INTO nodes (node_id, description, reverse_ssh_port) VALUES ('%s', '%s', %d)" % ( node_id, description, port ))


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
        if 'reverse_ssh_port' in node_database[node_id]:
            port = node_database[node_id]['reverse_ssh_port']
            permitopen = 'permitopen="localhost:%d"' % (port)
            line="%s,%s %s" % (permitopen, auth_options, node_database[node_id]['pub'])
            print line ,  "\n"
            new_authorized_keys_content.append(line)
            
    
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
    
    
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", httpserver_port))
    app.run()




