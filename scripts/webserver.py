#!/usr/bin/env python
import web, os.path, logging, re, urlparse, sys
from export import export_generator
# conatiner
#docker run -it  -v ${DATA}/export:/export --link beehive-cassandra:cassandra --rm -p 80:80 waggle/beehive-server /bin/bash

LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - line=%(lineno)d - %(message)s'
formatter = logging.Formatter(LOG_FORMAT)

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logging.getLogger('export').setLevel(logging.DEBUG)

port = 80
#port = 3030

web.config.log_toprint = True


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
        
        for row in export_generator(node_id, '', True):
            yield row+"\n"



class export:        
    def GET(self, node_id):
        web.header('Content-type','text/plain')
        web.header('Transfer-Encoding','chunked')
        
        query = web.ctx.query.encode('ascii', 'ignore') #get rid of unicode
        if query:
            query = query[1:]
        #TODO parse query
        logger.info("query: %s", query)
        query_dict = urlparse.parse_qs(query)
        
        try:
            date = query_dict['date']
        except KeyError:
            logger.warning("date key not found")
            raise web.notfound()
            
        logger.info("date: %s", str(date))
        if date:
            r = re.compile('\d{4}-\d{1,2}-\d{1,2}')
            if r.match(date):
                logger.info("accepted date: %s" %(date))
    
                for row in export_generator(node_id, date, FALSE):
                    yield row+"\n"
            else:
                logger.warning("date format not correct")
                raise web.notfound()
        else:
            logger.warning("date is empty")
            raise web.notfound()

if __name__ == "__main__":
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))
    app.run()




