#!/usr/bin/env python
import web
import os.path
from export import export_generator
# conatiner
#docker run -it  -v ${DATA}/export:/export --link beehive-cassandra:cassandra --rm -p 80:80 waggle/beehive-server /bin/bash


port = 80
#port = 3030


def read_file( str ):
    print "read_file: "+str
    if not os.path.isfile(str) :
        return ""
    with open(str,'r') as file_:
        return file_.read().strip()
    return ""





urls = (
    '/api/1/nodes/(.+)/latest', 'nodes_latest',
    '/api/1/nodes/(.+)/export', 'export',
    '/', 'index'
)

app = web.application(urls, globals())

class index:        
    def GET(self):
        
        text = "This is the Waggle Beehive web server.\n\n\n" + \
                "    Available resources:\n\n"
        
        
        for i in range(0, len(urls), 2):
            text = text + "\n" + "    " +  urls[i]
        
        
        return text+"\n\n"


class nodes_latest:        
    def GET(self, node_id):
        
        query = web.ctx.query
        
        
        web.header('Content-type','text/plain')
        web.header('Transfer-Encoding','chunked')
        
        for row in export_generator(node_id):
            yield row
        
        



class export:        
    def GET(self, node_id):
        
        query = web.ctx.query
        nodeid=None
        
        
        return str(query)+" node_id: "+node_id

if __name__ == "__main__":
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))
    app.run()




