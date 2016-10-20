#!/usr/bin/env python
import datetime
import json
import logging
import os.path
import re
import requests
import sys
import time
import urlparse
import web
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


web_host = 'http://beehive1.mcs.anl.gov'

api_url_internal = 'http://beehive-api:5000/api/'
api_url = web_host+'/api/'


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
    '/nodes/(.+)/?',                'web_node_page',
    '/',                            'index',
    '/wcc/',                        'index_WCC'

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
        
        
        api_call = api_url+'1/nodes/'
        api_call_internal = api_url_internal+'1/nodes/'
        api_call_last_update = api_url_internal+'1/nodes_last_update/'
        
        try:
            req = requests.get( api_call_internal ) # , auth=('user', 'password')
        except Exception as e:
            msg = "Could not make request: %s" % (str(e))
            logger.error(msg)
            raise internalerror(msg)
        
        if req.status_code != 200:
            msg = "status code: %d" % (req.status_code)
            logger.error(msg)
            raise internalerror(msg)
        
        #logger.debug("req.json: %s" % ( str(req.json())) )
        
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
        print 'all_nodes: ', str(all_nodes)
        
        yield """
            <head>
                <style>
                    table {    border-collapse: collapse; }
                    table, td, th { border: 1px solid black; padding: 1px 5px;}
                </style>
            </head>
        """
        yield "<table>\n"
        
        # header row
        headings = ['name', 'node_id', 'description', 'hostname', 'location', 'last_updated']
        result_line = '<tr>' + ''.join(['<td><b>{}</b></td>'.format(x) for x in headings]) + '</tr>\n'
        #logger.debug("result_line: %s" % (result_line))
        yield result_line
       
        # one row per node
        if True:
            for node_id in all_nodes:
                
                node_obj = all_nodes[node_id]
                node_id = node_id.encode('ascii','replace').lower()
                
                description = ''
                if u'description' in node_obj:
                    if node_obj[u'description']:
                        description = node_obj[u'description'].encode('ascii','replace')
                    
                hostname = ''
                if u'hostname' in node_obj:
                    if node_obj[u'hostname']:
                        hostname = node_obj[u'hostname'].encode('ascii','replace')

                name = ''
                if u'name' in node_obj:
                    if node_obj[u'name']:
                        name = node_obj[u'name'].encode('ascii','replace')
                        
                location = ''
                if u'location' in node_obj:
                    if node_obj[u'location']:
                        location = node_obj[u'location'].encode('ascii','replace')
                
                # last_updated contains its own <td> and </td> because it modifies them for color
                # eg. <td style="background-color:#FF0000">
                last_updated = '<td></td>'
                if False: #node_id in dictLastUpdate:
                    last_updated = '<td>%s</td>' % dictLastUpdate[node_id].encode('ascii','replace')
                
                #&nbsp&nbsp&nbsp&nbsp
                result_line = '<tr><td>%s</td><td><a href="%s/nodes/%s"><tt>%s</tt></a></td><td>%s</td><td>%s</td><td>%s</td>%s</tr>\n' % \
                    (name, web_host, node_id, node_id.upper(), description, hostname, location, last_updated)
                                
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


class index_WCC:        
    def GET(self):
        logger.debug('GET index_WCC')
        
        
        api_call = api_url+'1/nodes/'
        api_call_internal = api_url_internal+'1/nodes/'
        api_call_last_update = api_url_internal+'1/nodes_last_update/'
        
        try:
            req = requests.get( api_call_internal ) # , auth=('user', 'password')
        except Exception as e:
            msg = "Could not make request: %s" % (str(e))
            logger.error(msg)
            raise internalerror(msg)
        
        if req.status_code != 200:
            msg = "status code: %d" % (req.status_code)
            logger.error(msg)
            raise internalerror(msg)
        
        #logger.debug("req.json: %s" % ( str(req.json())) )

        # request last_update
        try:
            req_last_update = requests.get( api_call_last_update ) # , auth=('user', 'password')
        except Exception as e:
            msg = "Could not make request: %s: %s" % (api_call_last_update, str(e))
            logger.error(msg)
            raise internalerror(msg)
        
        if req_last_update.status_code != 200:
            msg = "status code: %d" % (req_last_update.status_code)
            logger.error(msg)
            raise internalerror(msg)
        
        dictLastUpdate = req_last_update.json()
        
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
        print 'all_nodes: ', str(all_nodes)
        
        yield """
            <head>
                <style>
                    table {    border-collapse: collapse; }
                    table, td, th { border: 1px solid black; padding: 1px 5px;}
                </style>
            </head>
        """
        yield "<table>\n"
        
        # header row
        headings = ['name', 'node_id', 'description', 'hostname', 'location', 'last_updated']
        result_line = '<tr>' + ''.join(['<td><b>{}</b></td>'.format(x) for x in headings]) + '</tr>\n'
        #logger.debug("result_line: %s" % (result_line))
        yield result_line
       
        # one row per node
        if True:
            for node_id in all_nodes:
                
                node_obj = all_nodes[node_id]
                node_id = node_id.encode('ascii','replace').lower()
                
                description = ''
                if u'description' in node_obj:
                    if node_obj[u'description']:
                        description = node_obj[u'description'].encode('ascii','replace')
                    
                hostname = ''
                if u'hostname' in node_obj:
                    if node_obj[u'hostname']:
                        hostname = node_obj[u'hostname'].encode('ascii','replace')

                name = ''
                if u'name' in node_obj:
                    if node_obj[u'name']:
                        name = node_obj[u'name'].encode('ascii','replace')
                        
                location = ''
                if u'location' in node_obj:
                    if node_obj[u'location']:
                        location = node_obj[u'location'].encode('ascii','replace')
                
                # last_updated contains its own <td> and </td> because it modifies them for color
                # eg. <td style="background-color:#FF0000">
                last_updated = '<td></td>'
                if node_id in dictLastUpdate:
                    s = datetime.datetime.utcfromtimestamp(float(dictLastUpdate[node_id])/1000.0).isoformat(sep = ' ')
                    last_updated = '<td>{}</td>'.format(s)
                
                #&nbsp&nbsp&nbsp&nbsp
                result_line = '<tr><td>%s</td><td><a href="%s/nodes/%s"><tt>%s</tt></a></td><td>%s</td><td>%s</td><td>%s</td>%s</tr>\n' % \
                    (name, web_host, node_id, node_id.upper(), description, hostname, location, last_updated)
                                
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
        
        api_call            = '%s1/nodes/%s/dates' % (api_url, node_id)
        api_call_internal   = '%s1/nodes/%s/dates' % (api_url_internal, node_id)
        
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
        # not available right now. yield '<br>\n<a href="%s/1/nodes/%s/latest">[last 3 minutes]</a>' % (api_url, node_id)
        
        logger.debug(str(req.json()))
        for date in req.json()['data']:
            yield '<br>\n<a href="%s1/nodes/%s/export?date=%s">%s</a>' % (api_url, node_id, date, date)


        yield  "<br>\n<br>\n"
        
        yield "Corresponding API call to get available dates:<br>\n<pre>curl %s</pre>" % (api_call)
        
        yield  "<br>\n<br>\n<h3>Download examples:</h3>\n"
        
        examples='''
<pre>
# get data from two specific days
for date in 2016-01-26 2016-01-27 ; do
&nbsp&nbsp&nbsp&nbsp curl -o {0}_${{date}}.csv {1}1/nodes/{0}/export?date=${{date}}
&nbsp&nbsp&nbsp&nbsp sleep 3
done

# get all data of one node
DATES=$(curl {1}1/nodes/{0}/dates | grep -o "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]")
for date in ${{DATES}} ; do
&nbsp&nbsp&nbsp&nbsp curl -o {0}_${{date}}.csv {1}1/nodes/{0}/export?date=${{date}}
&nbsp&nbsp&nbsp&nbsp sleep 3
done
</pre>
'''
        yield examples.format(node_id, api_url)
        
        yield "<br>\n<br>\n"

        yield html_footer()



if __name__ == "__main__":
    
    
    
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))
    app.internalerror = internalerror
    app.run()




