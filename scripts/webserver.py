#!/usr/bin/env python
import web, os.path, logging, re, urlparse, sys, json, requests
from export import export_generator, list_node_dates
# container
# docker run -it  --link beehive-cassandra:cassandra --rm -p 80:80 waggle/beehive-server /usr/lib/waggle/beehive-server/scripts/webserver.py 
# optional: -v ${DATA}/export:/export

LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - line=%(lineno)d - %(message)s'
formatter = logging.Formatter(LOG_FORMAT)

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logging.getLogger('export').setLevel(logging.DEBUG)


port = 80
self_url = 'http://beehive1.mcs.anl.gov'
api_url = 'http://beehive1.mcs.anl.gov'

# modify /etc/hosts/: 127.0.0.1	localhost beehive1.mcs.anl.gov

web.config.log_toprint = True


def read_file( str ):
    print "read_file: "+str
    if not os.path.isfile(str) :
        return ""
    with open(str,'r') as file_:
        return file_.read().strip()
    return ""


# TODO
# show API calls on the web pages !


urls = (
    '/api/1/nodes/(.+)/latest',     'api_nodes_latest',
    '/api/1/nodes/(.+)/export',     'api_export',
    '/api/1/nodes/(.+)/dates',      'api_dates',
    '/api/1/nodes/?',               'api_nodes',
    '/nodes/(.+)/?',                'web_node_page',
    '/',                            'index'
)

app = web.application(urls, globals())


def html_header(title):
    header= '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{0}</title>
</head>
<body>
'''
    return header.format(title)
 
def html_footer():
    return '''
</body>
</html>
'''
    
class index:        
    def GET(self):
        
        web.header('Content-type','text/html')
        web.header('Transfer-Encoding','chunked')
        
        yield html_header('Beehive web server')
        
        yield "<h2>This is the Waggle Beehive web server.</h2><br><br>\n\n"
        
        yield "Public nodes:<br>\n"
        
        api_call = api_url+'/api/1/nodes/'
        
        try:
            req = requests.get( api_call ) # , auth=('user', 'password')
        except Exception as e:
            logger.error("Could not make request: %s", (str(e)))
            raise web.internalerror()
        
        logger.debug("req.json: %s" % ( str(req.json())) )
        
        if not u'data' in req.json():
            logger.error("data field not found")
            raise web.internalerror()
        
        for node_id in req.json()[u'data']:
            yield '&nbsp&nbsp&nbsp&nbsp<a href="%s/nodes/%s">%s</a><br>\n' % (self_url, node_id, node_id)
        
        
        yield  "<br>\n<br>\n"
        
        yield "Corresponding API call to get list of nodes:<br>\n<pre>curl %s</pre>" % (api_call)
        
        yield  "<br>\n<br>\n"
        
        yield "<br><br>API resources:<br><br>\n\n"
        
        
        for i in range(0, len(urls), 2):
            yield  "&nbsp&nbsp&nbsp&nbsp" +  urls[i] + "<br>\n"
        
        
        yield html_footer()
        
class web_node_page:
    def GET(self, node_id):
       
        
        api_call = '%s/api/1/nodes/%s/dates' % (api_url, node_id)
        
        try:
            req = requests.get( api_call ) # , auth=('user', 'password')
        except Exception as e:
            logger.error("Could not make request: %s", (str(e)))
            raise web.internalerror()
            
        if not 'data' in req.json():
            raise web.internalerror()
        
        web.header('Content-type','text/html')
        web.header('Transfer-Encoding','chunked')
        
        #TODO check that node_id exists!
        yield html_header('Node '+node_id)
        yield "<h2>Node "+node_id+"</h2>\n\n\n"
        
        
        yield "Available data<br>\n"
        yield '<br>\n<a href="%s/api/1/nodes/%s/latest">[last 3 minutes]</a>' % (api_url, node_id)
        
        logger.debug(str(req.json()))
        for date in req.json()['data']:
            yield '<br>\n<a href="%s/api/1/nodes/%s/export?date=%s">%s</a>' % (api_url, node_id, date, date)


        yield  "<br>\n<br>\n"
        
        yield "Corresponding API call to get available dates:<br>\n<pre>curl %s</pre>" % (api_call)
        
        yield  "<br>\n<br>\n Download examples:<br>\n"
        
        examples='''
        <pre>
        # get data from two specific days<br>
        for date in 2016-01-26 2016-01-27 ; do <br>
        &nbsp&nbsp&nbsp&nbsp curl -O {0}_${{date}}.csv http://beehive1.mcs.anl.gov/api/1/nodes/{0}/export?date=${{date}} <br>
        &nbsp&nbsp&nbsp&nbsp sleep 3 <br>
        done <br>
         <br>
        # get all data of one node <br>
        DATES=$(curl http://beehive1.mcs.anl.gov/api/1/nodes/{0}/dates | grep -o "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]") <br>
        for date in ${DATES} ; do <br>
        &nbsp&nbsp&nbsp&nbsp curl -O {0}_${{date}}.csv http://beehive1.mcs.anl.gov/api/1/nodes/{0}/export?date=${{date}} <br>
        &nbsp&nbsp&nbsp&nbsp sleep 3 <br>
        done <br>
        </pre>
        '''
        yield examples.format(node_id)
        
        yield "<br><br>API resources:<br><br>\n\n"

        yield html_footer()

class api_nodes:        
    def GET(self):
        
        #query = web.ctx.query
        
        
        #web.header('Content-type','text/plain')
        #web.header('Transfer-Encoding','chunked')
        
        nodes_dict = list_node_dates()
        
        obj = {}
        obj['data'] = nodes_dict.keys()
        
        return  json.dumps(obj, indent=4)
        
            
class api_dates:        
    def GET(self, node_id):
        
        query = web.ctx.query
        
        nodes_dict = list_node_dates()
        
        if not node_id in nodes_dict:
            raise web.notfound()
        
        
        obj = {}
        obj['data'] = nodes_dict[node_id]
        
        return json.dumps(obj, indent=4)
        
        
        
                        

class api_nodes_latest:        
    def GET(self, node_id):
        
        query = web.ctx.query
        
        
        web.header('Content-type','text/plain')
        web.header('Transfer-Encoding','chunked')
        
        for row in export_generator(node_id, '', True):
            yield row+"\n"



class api_export:        
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
            date_array = query_dict['date']
        except KeyError:
            logger.warning("date key not found")
            raise web.notfound()
        
        if len(date_array) == 0:
            logger.warning("date_array empty")
            raise web.notfound()
        date = date_array[0]
            
        logger.info("date: %s", str(date))
        if date:
            r = re.compile('\d{4}-\d{1,2}-\d{1,2}')
            if r.match(date):
                logger.info("accepted date: %s" %(date))
    
                for row in export_generator(node_id, date, False):
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




