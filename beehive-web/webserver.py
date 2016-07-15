#!/usr/bin/env python
import web, os.path, logging, re, urlparse, sys, json, requests, time
from export import export_generator, list_node_dates
sys.path.append("..")
from waggle_protocol.utilities.mysql import *
# container
# docker run -it --name=beehive-web --link beehive-cassandra:cassandra --net beehive --rm -p 80:80 waggle/beehive-server /usr/lib/waggle/beehive-server/scripts/webserver.py 
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
#api_url_internal = 'http://localhost'
api_url_internal = 'http://beehive-api'
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
    '/api/1/epoch',                 'api_epoch',
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


def internalerror(e):
    
    message = html_header("Error") + "Sorry, there was an error:<br>\n<pre>\n"+str(e) +"</pre>\n"+ html_footer()
    
    return web.internalerror(message)
    

def get_mysql_db():
    return Mysql( host="beehive-mysql",    
                    user="waggle",       
                    passwd="waggle",  
                    db="waggle")


class index:        
    def GET(self):
        logger.debug('GET index')
        
        
        api_call = api_url+'/api/1/nodes/'
        api_call_internal = api_url_internal+'/api/1/nodes/'
        
        try:
            req = requests.get( api_call_internal ) # , auth=('user', 'password')
        except Exception as e:
            msg = "Could not make request: %s", (str(e))
            logger.error(msg)
            raise internalerror(msg)
        
        if req.status_code != 200:
            msg = "status code: %d" % (req.status_code)
            logger.error(msg)
            raise internalerror(msg)
        
        logger.debug("req.json: %s" % ( str(req.json())) )
        
        
        web.header('Content-type','text/html')
        web.header('Transfer-Encoding','chunked')
        
        yield html_header('Beehive web server')
        
        yield "<h2>This is the Waggle Beehive web server.</h2><br><br>\n\n"
        
        yield "<h3>Public nodes:</h3>\n"
        
        
        if not u'data' in req.json():
            msg = "data field not found"
            logger.error(msg)
            raise internalerror(msg)
        
        all_nodes = req.json()[u'data']
        
        
        yield "<table>\n"
        for node_id in all_nodes:
            
            node_obj = all_nodes[node_id]
            node_id = node_id.encode('ascii','replace').lower()
            logger.debug("node_id: %s" % (node_id))
            logger.debug("node_obj: %s" % (str(node_obj)))
            
            description = ''
            if u'description' in node_obj:
                if node_obj[u'description']:
                    description = node_obj[u'description'].encode('ascii','replace')
           
                
            hostname = ''
            if u'hostname' in node_obj:
                if node_obj[u'hostname']:
                    hostname = node_obj[u'hostname'].encode('ascii','replace')
            
            #&nbsp&nbsp&nbsp&nbsp
            result_line = '<tr><td><a href="%s/nodes/%s"><tt>%s</tt></a></td><td>%s</td><td>%s</td></tr>\n' % (api_url, node_id, node_id.upper(), description, hostname)
            
            logger.debug("result_line: %s" % (result_line))
            
            
            yield result_line
        
        yield "</table>"
        yield  "<br>\n<br>\n"
        
        yield "Corresponding API call to get list of nodes:<br>\n<pre>curl %s</pre>" % (api_call)
        
        yield  "<br>\n<br>\n"
        
        yield "<br><br><h3>API resources:</h3><br>\n\n"
        
        
        for i in range(0, len(urls), 2):
            if urls[i].startswith('/api'):
                yield  "&nbsp&nbsp&nbsp&nbsp" +  urls[i] + "<br>\n"
        
        
        yield html_footer()
        
class web_node_page:
    def GET(self, node_id):
        logger.debug('GET web_node_page')
        
        api_call            = '%s/api/1/nodes/%s/dates' % (api_url, node_id)
        api_call_internal   = '%s/api/1/nodes/%s/dates' % (api_url_internal, node_id)
        
        try:
            req = requests.get( api_call_internal ) # , auth=('user', 'password')
        except Exception as e:
            msg = "Could not make request: %s", (str(e))
            logger.error(msg)
            raise internalerror(msg)
        
        if req.status_code != 200:
            msg = "status code: %d" % (req.status_code)
            logger.error(msg)
            raise internalerror(msg)
            
        try:
            dates = req.json()
        except ValueError:
            logger.debug("Not json: " + str(req))
            raise internalerror("not found")
           
        if not 'data' in dates:
            logger.debug("data field not found")
            raise internalerror("not found")
        
        web.header('Content-type','text/html')
        web.header('Transfer-Encoding','chunked')
        
        #TODO check that node_id exists!
        yield html_header('Node '+node_id.upper())
        yield "<h2>Node "+node_id.upper()+"</h2>\n\n\n"
        
        
        yield "<h3>Available data</h3>\n"
        # not available right now. yield '<br>\n<a href="%s/api/1/nodes/%s/latest">[last 3 minutes]</a>' % (api_url, node_id)
        
        logger.debug(str(req.json()))
        for date in req.json()['data']:
            yield '<br>\n<a href="%s/api/1/nodes/%s/export?date=%s">%s</a>' % (api_url, node_id, date, date)


        yield  "<br>\n<br>\n"
        
        yield "Corresponding API call to get available dates:<br>\n<pre>curl %s</pre>" % (api_call)
        
        yield  "<br>\n<br>\n<h3>Download examples:</h3>\n"
        
        examples='''
<pre>
# get data from two specific days
for date in 2016-01-26 2016-01-27 ; do
&nbsp&nbsp&nbsp&nbsp curl -o {0}_${{date}}.csv {1}/api/1/nodes/{0}/export?date=${{date}}
&nbsp&nbsp&nbsp&nbsp sleep 3
done

# get all data of one node
DATES=$(curl {1}/api/1/nodes/{0}/dates | grep -o "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]")
for date in ${{DATES}} ; do
&nbsp&nbsp&nbsp&nbsp curl -o {0}_${{date}}.csv {1}/api/1/nodes/{0}/export?date=${{date}}
&nbsp&nbsp&nbsp&nbsp sleep 3
done
</pre>
'''
        yield examples.format(node_id, api_url)
        
        yield "<br>\n<br>\n"

        yield html_footer()


class api_epoch:
    """
    Epoch time in seconds.
    """

    def GET(self):
        logger.debug('GET api_epoch')

        try:
            epoch= int(time.time())
        except:
            raise internalerror('error getting server time')
            
            
        return '{"epoch": "deprecated"}'
        #return '{"epoch": %d}' % (epoch)


class api_nodes:        
    def GET(self):
        logger.debug('GET api_nodes')
        #query = web.ctx.query
        
        
        #web.header('Content-type','text/plain')
        #web.header('Transfer-Encoding','chunked')
        
        db = get_mysql_db()
        
        all_nodes = {}
        mysql_nodes_result = db.query_all("SELECT node_id,hostname,project,description,reverse_ssh_port FROM nodes;")
        for result in mysql_nodes_result:
            node_id, hostname, project, description, reverse_ssh_port = result
            
            if node_id:
                node_id = node_id.encode('ascii','replace').lower()
            else:
                node_id = 'unknown'
                
            if hostname:
                hostname = hostname.encode('ascii','replace')
                
            if description:
                description = description.encode('ascii','replace')
                
            
            
            logger.debug('got from mysql: %s %s %s %s %s' % (node_id, hostname, project, description, reverse_ssh_port))
            all_nodes[node_id] = {  'hostname'          : hostname,
                                    'project'           : project, 
                                    'description'       : description ,
                                    'reverse_ssh_port'  : reverse_ssh_port }
            
        
        
        nodes_dict = list_node_dates() # lower case
        
        for node_id in nodes_dict.keys():
            if not node_id in all_nodes:
                all_nodes[node_id]={}
        
        #for node_id in all_nodes.keys():
        #    logger.debug("%s %s" % (node_id, type(node_id)))
        
        obj = {}
        obj['data'] = all_nodes
        
        return  json.dumps(obj, indent=4)
        
            
class api_dates:        
    def GET(self, node_id):
        logger.debug('GET api_dates')
        
        node_id = node_id.lower()
        
        query = web.ctx.query
        
        nodes_dict = list_node_dates()
        
        if not node_id in nodes_dict:
            logger.debug("node_id not found in nodes_dict: " + node_id)
            raise web.notfound()
        
        dates = nodes_dict[node_id]
        
        logger.debug("dates: " + str(dates))
        
        obj = {}
        obj['data'] = sorted(dates, reverse=True)
        
        return json.dumps(obj, indent=4)
        
        
        
                        

class api_nodes_latest:        
    def GET(self, node_id):
        logger.debug('GET api_nodes_latest')
        
        query = web.ctx.query
        
        
        web.header('Content-type','text/plain')
        web.header('Transfer-Encoding','chunked')
        
        #for row in export_generator(node_id, '', True, ';'):
        #    yield row+"\n"
        yield "not implemented"



class api_export:        
    def GET(self, node_id):
        
        logger.debug('GET api_export')
        
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
    
                num_lines = 0
                for row in export_generator(node_id, date, False, ';'):
                    yield row+"\n"
                    num_lines += 1
                
                if num_lines == 0:
                    raise web.notfound()
                else:
                    yield "# %d results" % (num_lines)
            else:
                logger.warning("date format not correct")
                raise web.notfound()
        else:
            logger.warning("date is empty")
            raise web.notfound()

if __name__ == "__main__":
    
    
    
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))
    app.internalerror = internalerror
    app.run()




