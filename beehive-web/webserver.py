#!/usr/bin/env python
import datetime
import itertools
import json
import logging
import operator
import os.path
import re
import requests
import sys
import time
import urlparse
import web
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
    '/wcc/',                        'index_WCC',
    '/test/',                       'test'

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


class test:        
    def GET(self):
        logger.debug('GET test')
        
        
        form = web.input(debug = 'false')
        
        message = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>This is the title</title>
</head>
<body>
<h1>Beehive Web-Server Test Page</h1>
<br></\br>
UTC timestamp = {0}
<br></br>
debug = {1}
</body>
</html>
'''
        dtUtcNow = datetime.datetime.utcnow()
        yield message.format(dtUtcNow, form.debug)

                    
                    
class index:        
    def GET(self):
        logger.debug('GET index')
        
        user_data = web.input(all="false")
        allNodes_arg = '?all=true' # if user_data.all else ''

        api_call = api_url + '1/nodes/' + allNodes_arg
        api_call_internal = api_url_internal + '1/nodes/' + allNodes_arg
        api_call_last_update = api_url_internal+'1/nodes_last_update/'
        
        dtUtcNow = datetime.datetime.utcnow()

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
        yield "<p><i> UTC of last update of this page:</i> {}</p>\n".format(
            dtUtcNow.strftime("%Y-%m-%d %H:%M:%S"))
        
        if not u'data' in req.json():
            msg = "data field not found"
            logger.error(msg)
            raise internalerror(msg)

        all_nodes = req.json()[u'data']
        #print 'all_nodes: ', str(all_nodes)
        
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
        headings = ['name', 'node_id', 'v2 data', 'description', 'hostname', 'location', 'last_updated']
        result_line = '<tr>' + ''.join(['<td><b>{}</b></td>'.format(x) for x in headings]) + '</tr>\n'
        #logger.debug("result_line: %s" % (result_line))
        yield result_line
       
        # list of tuples.  1st number is dt, 2nd is color.  Must be sorted in order of decreasing times.
        # find the first timedelta that is smaller than the data's timestamp's 
        timeToColors = [    
            (datetime.timedelta(days = 1), '#ff3333'),      # dead = red
            (datetime.timedelta(hours = 2), '#ff8000'),     # dying = orange
            (datetime.timedelta(minutes = 5), '#ffff00'),   # just starting to die = yellow
            (datetime.timedelta(seconds = 0), '#00ff00'),   # live = green
            (datetime.timedelta(seconds = -1), '#ff00ff'),   # future!!! (time error) = magenta
        ]
        # one row per node
        

        nodes_sorted = list()
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

            nodes_sorted.append((node_id, name, description, location, hostname))
                        
        # sort the list
        def EmptyStringsLast(v):
            return v if v != '' else 'ZZZZZZ'
        def MyKey(x):
            return (EmptyStringsLast(x[1]), EmptyStringsLast(x[2]), EmptyStringsLast(x[3]), EmptyStringsLast(x[0]))
            
        nodes_sorted.sort(key = lambda x: MyKey(x))
        
        durations = [
            ('year', datetime.timedelta(days = 365).total_seconds()),
            ('month', datetime.timedelta(days = 30).total_seconds()),
            ('week', datetime.timedelta(days = 7).total_seconds()),
            ('day', datetime.timedelta(days = 1).total_seconds()),
            ('hour', datetime.timedelta(seconds = 3600).total_seconds()),
            ('minute', datetime.timedelta(seconds = 60).total_seconds()),
        ]
                    
        for node_tuple in nodes_sorted:
            node_id, name, description, location, hostname = node_tuple
            # last_updated contains its own <td> and </td> because it modifies them for color
            # eg. <td style="background-color:#FF0000">
            last_updated = '<td></td>'
            duration_string = ''
            if node_id in dictLastUpdate:
                dt = datetime.datetime.utcfromtimestamp(float(dictLastUpdate[node_id])/1000.0) 
                #s = dt.isoformat(sep = ' ')
                s = dt.strftime("%Y-%m-%d %H:%M:%S")
                delta = dtUtcNow - dt
                color = timeToColors[-1][1] # negative time - should correspond to last value
                for tuple in timeToColors:
                    if delta > tuple[0]:
                        color = tuple[1]
                        break

                # human-readable duration
                duration_string = '1 minute ago'
                delta_seconds = delta.total_seconds()

                for dur in durations:
                    if delta_seconds >= dur[1]:
                        num = int(delta_seconds / dur[1])
                        duration_string = '{} {}{} ago'.format(num, dur[0], '' if num < 2 else 's')
                        break
                last_updated = '<td style="background-color:{}"><tt>{}</tt> &nbsp <b>({})</b></td>'.format(color, s, duration_string)
                        
            #&nbsp&nbsp&nbsp&nbsp
            result_line = '''<tr>
                <td align="right"><tt>%s</tt></td>
                <td><a href="%s/nodes/%s?version=1"><tt>%s</tt></a></td>
                <td><a href="%s/nodes/%s?version=2"><tt>v2</tt></a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                %s
                </tr>\n'''                \
                % (name, web_host, node_id, node_id.upper(), web_host, node_id, description, hostname, location, last_updated)
                            
            yield result_line


class index_WCC:        
    def GET(self):
        logger.debug('GET index_WCC')
        
        user_data = web.input(all="false")
        allNodes_arg = '?all=true' if user_data.all else ''

        api_call = api_url + '1/nodes/' + allNodes_arg
        api_call_internal = api_url_internal + '1/nodes/' + allNodes_arg
        api_call_last_update = api_url_internal+'1/nodes_last_update/'
        
        dtUtcNow = datetime.datetime.utcnow()

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
        yield "<p><i> UTC of last update of this page:</i> {}</p>\n".format(
            dtUtcNow.strftime("%Y-%m-%d %H:%M:%S"))
        
        if not u'data' in req.json():
            msg = "data field not found"
            logger.error(msg)
            raise internalerror(msg)

        all_nodes = req.json()[u'data']
        #print 'all_nodes: ', str(all_nodes)
        
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
        headings = ['name', 'node_id', 'v2 data', 'description', 'hostname', 'location', 'last_updated']
        result_line = '<tr>' + ''.join(['<td><b>{}</b></td>'.format(x) for x in headings]) + '</tr>\n'
        #logger.debug("result_line: %s" % (result_line))
        yield result_line
       
        # list of tuples.  1st number is dt, 2nd is color.  Must be sorted in order of decreasing times.
        # find the first timedelta that is smaller than the data's timestamp's 
        timeToColors = [    
            (datetime.timedelta(days = 1), '#ff3333'),      # dead = red
            (datetime.timedelta(hours = 2), '#ff8000'),     # dying = orange
            (datetime.timedelta(minutes = 5), '#ffff00'),   # just starting to die = yellow
            (datetime.timedelta(seconds = 0), '#00ff00'),   # live = green
            (datetime.timedelta(seconds = -1), '#ff00ff'),   # future!!! (time error) = magenta
        ]
        # one row per node
        

        nodes_sorted = list()
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

            nodes_sorted.append((node_id, name, description, location, hostname))
                        
        # sort the list
        def EmptyStringsLast(v):
            return v if v != '' else 'ZZZZZZ'
        def MyKey(x):
            return (EmptyStringsLast(x[1]), EmptyStringsLast(x[2]), EmptyStringsLast(x[3]), EmptyStringsLast(x[0]))
            
        nodes_sorted.sort(key = lambda x: MyKey(x))
        
        durations = [
            ('year', datetime.timedelta(days = 365).total_seconds()),
            ('month', datetime.timedelta(days = 30).total_seconds()),
            ('week', datetime.timedelta(days = 7).total_seconds()),
            ('day', datetime.timedelta(days = 1).total_seconds()),
            ('hour', datetime.timedelta(seconds = 3600).total_seconds()),
            ('minute', datetime.timedelta(seconds = 60).total_seconds()),
        ]
                    
        for node_tuple in nodes_sorted:
            node_id, name, description, location, hostname = node_tuple
            # last_updated contains its own <td> and </td> because it modifies them for color
            # eg. <td style="background-color:#FF0000">
            last_updated = '<td></td>'
            duration_string = ''
            if node_id in dictLastUpdate:
                dt = datetime.datetime.utcfromtimestamp(float(dictLastUpdate[node_id])/1000.0) 
                #s = dt.isoformat(sep = ' ')
                s = dt.strftime("%Y-%m-%d %H:%M:%S")
                delta = dtUtcNow - dt
                color = timeToColors[-1][1] # negative time - should correspond to last value
                for tuple in timeToColors:
                    if delta > tuple[0]:
                        color = tuple[1]
                        break

                # human-readable duration
                duration_string = '1 minute ago'
                delta_seconds = delta.total_seconds()

                for dur in durations:
                    if delta_seconds >= dur[1]:
                        num = int(delta_seconds / dur[1])
                        duration_string = '{} {}{} ago'.format(num, dur[0], '' if num < 2 else 's')
                        break
                last_updated = '<td style="background-color:{}"><tt>{}</tt> &nbsp <b>({})</b></td>'.format(color, s, duration_string)
                        
            #&nbsp&nbsp&nbsp&nbsp
            result_line = '''<tr>
                <td align="right"><tt>%s</tt></td>
                <td><a href="%s/nodes/%s?version=1"><tt>%s</tt></a></td>
                <td><a href="%s/nodes/%s?version=2"><tt>v2</tt></a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                %s
                </tr>\n'''                \
                % (name, web_host, node_id, node_id.upper(), web_host, node_id, description, hostname, location, last_updated)
                            
            yield result_line


        
class web_node_page:
    def GET(self, node_id):
        logger.debug('GET web_node_page')
        
        user_data = web.input(version = '1')
        version = user_data.version
        
        logger.debug('#######     web_node_page.... version = ' + version)

        api_call            = '%s1/nodes/%s/dates?version=%s' % (api_url, node_id, version)
        api_call_internal   = '%s1/nodes/%s/dates?version=%s' % (api_url_internal, node_id, version)
        
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
        
        
        yield "<h3>Available data - version %s </h3>\n" % version
        # not available right now. yield '<br>\n<a href="%s/1/nodes/%s/latest">[last 3 minutes]</a>' % (api_url, node_id)
        
        logger.debug('__web_node_page():  DATES FOUND:  ' + str(req.json()))
        
        yield str(req.json())
        
        
        for date in req.json()['data']:
            #yield date + '<br>\n'
            yield '<br>\n<a href="%s1/nodes/%s/export?date=%s&version=%s">%s</a>' % (api_url, node_id, date, version, date)

        yield  "<br>\n<br>\n"
        
        yield "Corresponding API call to get available dates:<br>\n<pre>curl %s</pre>" % (api_call)
        
        yield  "<br>\n<br>\n<h3>Download examples:</h3>\n"
        
        examples='''
<pre>
# get data from two specific days
for date in 2016-01-26 2016-01-27 ; do
&nbsp&nbsp&nbsp&nbsp curl -o {0}_${{date}}.csv {1}1/nodes/{0}/export?date=${{date}}&version={2}
&nbsp&nbsp&nbsp&nbsp sleep 3
done

# get all data of one node
DATES=$(curl {1}1/nodes/{0}/dates | grep -o "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]")
for date in ${{DATES}} ; do
&nbsp&nbsp&nbsp&nbsp curl -o {0}_${{date}}.csv {1}1/nodes/{0}/export?date=${{date}}&version={2}
&nbsp&nbsp&nbsp&nbsp sleep 3
done
</pre>
'''
        yield examples.format(node_id, api_url, version)
        
        yield "<br>\n<br>\n"

        yield html_footer()
        

if __name__ == "__main__":
    
    
    
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))
    app.internalerror = internalerror
    app.run()




