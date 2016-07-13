#!/usr/bin/env python3
import os.path, logging, re, urlparse, sys, json, requests, time
from export import export_generator, list_node_dates
sys.path.append("..")
from waggle_protocol.utilities.mysql import *

from flask import Flask
app = Flask(__name__)
from flask import Response
from flask import request
from flask import jsonify

# pip3 install Flask

# container
# docker run -it --name=beehive-api --link beehive-cassandra:cassandra --net beehive --rm -p 8183:80 waggle/beehive-server /usr/lib/waggle/beehive-server/scripts/apiserver.py 
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
api_url_internal = 'http://localhost'
api_url = 'http://beehive1.mcs.anl.gov'

# modify /etc/hosts/: 127.0.0.1	localhost beehive1.mcs.anl.gov



STATUS_Bad_Request = 400 # A client error
STATUS_Unauthorized = 401
STATUS_Not_Found = 404
STATUS_Server_Error =  500


def read_file( str ):
    logger.debug("read_file: "+str)
    if not os.path.isfile(str) :
        return ""
    with open(str,'r') as file_:
        return file_.read().strip()
    return ""






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



class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code AND status_code==STATUS_Server_Error:
            logger.warning(message)
        else:
            logger.debug(message)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
        

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



def internalerror(e):
    
    message = html_header("Error") + "Sorry, there was an error:<br>\n<pre>\n"+str(e) +"</pre>\n"+ html_footer()
    
    return message
    

def get_mysql_db():
    return Mysql( host="beehive-mysql",    
                    user="waggle",       
                    passwd="waggle",  
                    db="waggle")


@app.route('/api/1/epoch')
def api_epoch:
    """
    Epoch time in seconds.
    """

    logger.debug('GET api_epoch')

    try:
        epoch= int(time.time())
    except:
        raise InvalidUsage('error getting server time', status_code=STATUS_Server_Error)
        
        
        
    return '{"epoch": %d}' % (epoch)


@app.route('/api/1/nodes/')
def api_nodes:        

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
    
@app.route('/api/1/nodes/<node_id>/dates')
def api_dates(node_id):        

    logger.debug('GET api_dates')
    
    node_id = node_id.lower()
    
    query = web.ctx.query
    
    nodes_dict = list_node_dates()
    
    if not node_id in nodes_dict:
        raise InvalidUsage("node_id not found in nodes_dict: " + node_id,  status_code=STATUS_Bad_Request )
    
    dates = nodes_dict[node_id]
    
    logger.debug("dates: " + str(dates))
    
    obj = {}
    obj['data'] = sorted(dates, reverse=True)
    
    return json.dumps(obj, indent=4)
    
        
        
                        



@app.route('/api/1/nodes/<node_id>/export')
def api_export(node_id):        
   
   
    def generate():
        logger.debug('GET api_export')
        
        date = request.args.get('date').encode('ascii', 'ignore') #get rid of unicode
       
        
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
                    raise InvalidUsage("num_lines == 0", status_code=STATUS_Server_Error)
                else:
                    yield "# %d results" % (num_lines)
            else:
            
                raise InvalidUsage("date format not correct", status_code=STATUS_Not_Found)
        else:
        
            raise InvalidUsage("date is empty", status_code=STATUS_Not_Found)
            
    return Response(generate(), mimetype='text/csv')

if __name__ == "__main__":
    
    
    
    #web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))
    #app.internalerror = internalerror
    #app.run()
    app.run()




