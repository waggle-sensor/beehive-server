#!/usr/bin/env python
import web
import os.path
import subprocess
import threading
import re

# docker run -ti -p 9999:9999 -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ --name cert-serve waggle/beehive-server /bin/bash
# cd /usr/lib/waggle/beehive-server/cert-serve ; ./cert-serve.py
# apt-get install python-webpy
# pip install web.py
# echo "unique_subject = no" > SSL/waggleca/index.txt.attr

resource_lock = threading.RLock()

ssl_path = "/usr/lib/waggle/beehive-server/SSL/"

hexaPattern = re.compile(r'^([0-9A-F]*)$')
prog = re.compile(hexaPattern)


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
            print "Using nodeid: "+str(nodeid)
            node_dir = ssl_path + 'node_'+ nodeid
            if not os.path.isdir(node_dir):
                with resource_lock:
                    subprocess.call([ssl_path + 'create_client_cert.sh', 'node', 'node_'+ nodeid])
            
            privkey = read_file(node_dir + '/key.pem')
            cert    = read_file(node_dir + '/cert.pem')       
        else:
            print "No nodeid provided."
            with resource_lock:
                subprocess.call([ssl_path + 'create_client_cert.sh', 'node', 'temp_client_cert'])
                privkey = read_file(ssl_path + 'temp_client_cert/key.pem')
                cert    = read_file(ssl_path + 'temp_client_cert/cert.pem')
            
        if not privkey:
            return "error: privkey file not found !?"
        
        if not cert:
            return "error: cert file not found !?"

        if nodeid:
            print "issuing cert for node "+nodeid
        else:
            print "issuing cert for unknown node"
        return privkey + "\n" + cert


if __name__ == "__main__":
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", 9999))
    app.run()




