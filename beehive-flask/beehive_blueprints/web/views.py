from . import web 
from flask import Response
from flask import request
from flask import jsonify
from flask import render_template
from flask import stream_with_context
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

api_url          = 'localhost:'
api_url_internal = 'localhost:'

@web.route('/')
def web_root():
    return 'You found web!!!'

@web.route("/wcc/test/")
def web_wcc_test():
    rl = [] # result list

    rl.append("<h1 style='color:green'>Hello There!</h1>")
    rl.append('args = ' + str(request.args))
    rl.append('<br>')
    d = request.args.to_dict()
    rl.append('to_dict = ' + str(d))
    rl.append('<br>')
    rl.append('<br>')
    rl.append('items:  ' + str(d.items()))
    rl.append('<br>')
    rl.append('<br>')
    for x in d.keys():
        rl.append('   {} : {} <br>'.format(x, d[x]))
    debug = request.args.get('debug', 'False')
    rl.append('<br>')
    rl.append('debug :  {}'.format(debug))
    return ''.join(rl)
    

@web.route("/wcc/")
def main_page():

    allNodes_arg = '?all=true' if (request.args.get('all', 'false').lower() == 'true') else ''

    api_call = api_url + '1/nodes/' + allNodes_arg
    api_call_internal = api_url_internal + '1/nodes/' + allNodes_arg
    api_call_last_update = api_url_internal+'1/nodes_last_update/'
    
    dtUtcNow = datetime.datetime.utcnow()

    req = None
    try:
        req = requests.get( api_call_internal ) # , auth=('user', 'password')
    except Exception as e:
        msg = "Could not make request: %s" % (str(e))
        logger.error(msg)
        #raise internalerror(msg)
    
    if req and req.status_code != 200:
        msg = "status code: %d" % (req.status_code)
        logger.error(msg)
        #raise internalerror(msg)
    
    #logger.debug("req.json: %s" % ( str(req.json())) )

    # request last_update
    req_last_update = None
    try:
        req_last_update = requests.get( api_call_last_update ) # , auth=('user', 'password')
    except Exception as e:
        msg = "Could not make request: %s: %s" % (api_call_last_update, str(e))
        logger.error(msg)
        #raise internalerror(msg)
    
    if req_last_update and req_last_update.status_code != 200:
        msg = "status code: %d" % (req_last_update.status_code)
        logger.error(msg)
        #raise internalerror(msg)
    
    dictLastUpdate = req_last_update.json()
    
    listRows = []
        
    if not u'data' in req.json():
        msg = "data field not found"
        logger.error(msg)
        #raise internalerror(msg)

    all_nodes = req.json()[u'data']
   
    # header row
    headings = ['name', 'node_id', 'description', 'hostname', 'location', 'last_updated']
    listRows.append('<tr>' + ''.join(['<td align="center"><b>{}</b></td>'.format(x) for x in headings]) + '</tr>\n')
   
    # list of tuples.  1st number is dt, 2nd is color.  Must be sorted in order of decreasing times.
    # find the first timedelta that is smaller than the data's timestamp's 
    timeToColors = [    
        (datetime.timedelta(days = 1),  '#ff3333'),      # dead = red
        (datetime.timedelta(hours = 2), '#ff8000'),     # dying = orange
        (datetime.timedelta(minutes = 5), '#ffff00'),   # just starting to die = yellow
        (datetime.timedelta(seconds = 0), '#00ff00'),   # live = green
        (datetime.timedelta(seconds = -1), '#ff00ff'),   # future!!! (time error) = magenta
    ]
    # one row per node

    nodes_sorted = list()
    for node_id in all_nodes:

        node_obj = all_nodes[node_id]
        node_id = node_id.encode('ascii','replace').lower().decode()

        description = ''
        if u'description' in node_obj:
            if node_obj[u'description']:
                description = node_obj[u'description'].encode('ascii','replace').decode()
            
        hostname = ''
        if u'hostname' in node_obj:
            if node_obj[u'hostname']:
                hostname = node_obj[u'hostname'].encode('ascii','replace').decode()

        name = ''
        if u'name' in node_obj:
            if node_obj[u'name']:
                name = node_obj[u'name'].encode('ascii','replace').decode()
                
        location = ''
        if u'location' in node_obj:
            if node_obj[u'location']:
                location = node_obj[u'location'].encode('ascii','replace').decode()

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
            last_updated = '<td align="left" style="background-color:{}"><b>{}</b> <tt>({})</tt></td>'.format(color, duration_string, s)
                    
        listRows.append('''<tr>
            <td align="right"><tt>%s</tt></td>
            <td><a href="%s/nodes/%s?version=1"><tt>%s</tt></a></td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            %s
            </tr>'''                \
            % (name, web_host, node_id, node_id, description, hostname, location, last_updated))
    
    return render_template('nodes.html', 
        api_call = api_call,
        api_url = api_url,
        utc_now = dtUtcNow.strftime("%Y-%m-%d %H:%M:%S"),
        list_rows = listRows)

    