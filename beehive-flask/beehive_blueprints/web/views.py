from . import web

from flask import Response
from flask import request
from flask import jsonify
from flask import render_template
from flask import stream_with_context

import datetime
import logging
import requests
import sys

sys.path.append("../..")
import export
sys.path.pop()

LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - line=%(lineno)d - %(message)s'
formatter = logging.Formatter(LOG_FORMAT)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logging.getLogger('export').setLevel(logging.DEBUG)

web_host = 'http://beehive1.mcs.anl.gov/'
api_url  = web_host + 'api/'

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

durations_human_readable = [
    ('yr', datetime.timedelta(days = 365).total_seconds()),
    ('mo', datetime.timedelta(days = 30).total_seconds()),
    ('wk', datetime.timedelta(days = 7).total_seconds()),
    ('d', datetime.timedelta(days = 1).total_seconds()),
    ('hr', datetime.timedelta(seconds = 3600).total_seconds()),
    ('m', datetime.timedelta(seconds = 60).total_seconds()),
]

def pretty_print_last_update(dtNow, timestampUpdate):
    if timestampUpdate == None:
        last_data = '<td></td>'
    else:
        duration_string = ''

        dt = datetime.datetime.utcfromtimestamp(float(timestampUpdate) / 1000.0)
        s = dt.strftime("%Y-%m-%d %H:%M:%S")
        delta = dtNow - dt
        if False: #bAllNodes:
            color = timeToColors[-1][1] # negative time - should correspond to last value
            for tuple in timeToColors:
                if delta > tuple[0]:
                    color = tuple[1]
                    break
        else:
            color = '#ffffff'
                
        # human readable duration
        sHuman = '1 m'
        delta_seconds = delta.total_seconds()

        for dur in durations_human_readable:
            if delta_seconds >= dur[1]:
                num = int(delta_seconds / dur[1])
                sHuman = '{} {}'.format(num, dur[0])
                break

        last_data = '<td align="left" style="background-color:{}"><b>{}</b> <tt>({})</tt></td>'.format(color, sHuman, s)
    return last_data
    
def pretty_print_last_update_dict(dtNow, timestampUpdate):
    d = {'human': '', 'timestamp':''}
    if timestampUpdate:
        dt = datetime.datetime.utcfromtimestamp(float(timestampUpdate) / 1000.0)
        d['timestamp'] = '({})'.format(dt.strftime("%Y-%m-%d %H:%M:%S"))
        delta = dtNow - dt
        if False: #bAllNodes:
            color = timeToColors[-1][1] # negative time - should correspond to last value
            for tuple in timeToColors:
                if delta > tuple[0]:
                    color = tuple[1]
                    break
        else:
            color = '#ffffff'
                
        # human readable duration
        sHuman = '1 m'
        delta_seconds = delta.total_seconds()

        for dur in durations_human_readable:
            if delta_seconds >= dur[1]:
                num = int(delta_seconds / dur[1])
                sHuman = '{} {}'.format(num, dur[0])
                break
        d['human'] = sHuman
    return d

@web.route("/")
def main_page():

    api_call = web_host + '/api/1/'

    # if bAllNodes ('b' is for 'bool') is True, print all nodes, otherwise filter the active ones
    bAllNodes = request.args.get('all', 'false').lower() == 'true'

    dtUtcNow = datetime.datetime.utcnow()
    deltaOfflineMin = datetime.timedelta(hours = 1) # minimum duration to keep a node offline

    # request last_update info
    lastUpdateTypes = ['data', 'log', 'ssh']
    dictLastUpdate = {t : export.get_nodes_last_update_dict(t) for t in lastUpdateTypes}
    dictOffline = export.get_nodes_offline_dict()

    listRows = []

    all_nodes = export.get_nodes(bAllNodes)

    # header row
    headings = ['Name/<br>VSN*', 'Node ID', 'Description', 'Location', 'Status', 'Last Connection', 'Last Data']
    if bAllNodes:  headings.extend(['Last SSH', 'Last Log'])
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
        """
        hostname = ''
        if u'hostname' in node_obj:
            if node_obj[u'hostname']:
                hostname = node_obj[u'hostname'].encode('ascii','replace').decode()
        """
        name = ''
        if u'name' in node_obj:
            if node_obj[u'name']:
                name = node_obj[u'name'].encode('ascii','replace').decode()

        location = ''
        if u'location' in node_obj:
            if node_obj[u'location']:
                location = node_obj[u'location'].encode('ascii','replace').decode()

        opmode = ''
        if u'opmode' in node_obj:
            if node_obj[u'opmode']:
                opmode = node_obj[u'opmode'].encode('ascii','replace').decode()

        nodes_sorted.append((node_id, name, description, location, opmode))

    # sort the list
    def EmptyStringsLast(v):
        return v if v != '' else 'ZZZZZZ'
    def MyKey(x):
        return (EmptyStringsLast(x[1]), EmptyStringsLast(x[2]), EmptyStringsLast(x[3]), EmptyStringsLast(x[0]))

    nodes_sorted.sort(key = lambda x: MyKey(x))

    for node_tuple in nodes_sorted:
        node_id, name, description, location, opmode = node_tuple
        
        last_data = pretty_print_last_update_dict(dtUtcNow, dictLastUpdate['data'].get(node_id))
        if bAllNodes:
            last_ssh  = pretty_print_last_update_dict(dtUtcNow, dictLastUpdate['ssh'].get(node_id))
            last_log  = pretty_print_last_update_dict(dtUtcNow, dictLastUpdate['log'].get(node_id))
        else:
            last_ssh = last_log = pretty_print_last_update_dict(dtUtcNow, None)

        # last connection (most recent of all 3 last_update's)
        latest = None
        for t in lastUpdateTypes:
            if node_id in dictLastUpdate[t]:
                if latest == None or dictLastUpdate[t][node_id] > latest:
                    latest = dictLastUpdate[t][node_id]

        if latest:
            dtLastConnection = datetime.datetime.utcfromtimestamp(float(latest)/1000.0)
        last_connection = pretty_print_last_update_dict(dtUtcNow, latest)

        # offline status 
        bOffline = False
        if node_id in dictOffline:
            dtOfflineStart = datetime.datetime.utcfromtimestamp(float(dictOffline[node_id]))
            dtOfflineEnd = dtOfflineStart + deltaOfflineMin
            print('node_id = {}, dtOfflineStart = {}, dtOfflineEnd = {} dtUtcNow = {}'.format(node_id, dtOfflineStart.strftime("%Y-%m-%d %H:%M:%S"), dtOfflineEnd.strftime("%Y-%m-%d %H:%M:%S"), dtUtcNow.strftime("%Y-%m-%d %H:%M:%S")))
            if dtUtcNow < dtOfflineEnd:
                # offline period has not expired yet
                bOffline = True
            elif latest == None:
                # no communication happened yet
                bOffline = True
            elif dtLastConnection < dtOfflineEnd:
                # the last communication was before the expiration period
                bOffline = True
            else:   # the last communication happened after the expiration period
                bOffline = False
                
            # clear the offline flag if it changed to False
            if not bOffline:
                print('############# CLEARING OFFLINE!!!!!!!!!!!!!!!!!!!!')
                export.set_node_offline(node_id, False)
                
        # compute the status
        status = {'color':'#ff00ff', 'label':'UNKNOWN'} #'<td align="center" style="background-color:#ff00ff">UNKNOWN</td>'
        if opmode.strip().lower() != 'production':
            #status = '<td align="center" style="background-color:#8888ff">{}</td>'.format(opmode.strip())  # this shouldn't print in generic user mode
            status = {'color':'#8888ff', 'label':opmode.strip()} 
        elif bOffline:
            #status = '<td align="center" style="background-color:#aaaaaa">Offline</td>'
            status = {'color':'#aaaaaa', 'label':'Offline'} 
        elif (latest and dtUtcNow - dtLastConnection < datetime.timedelta(days = 7)): 
            #status = '<td align="center" style="background-color:#00ff00">Alive</td>'
            status = {'color':'#00ff00', 'label':'Alive'} 
        else:
            #status = '<td align="center" style="background-color:#ff0000">Dead</td>'
            status = {'color':'#ff0000', 'label':'Dead'} 
        
        listRows.append({'name':name, 
            'node_id':node_id,
            'description':description, 
            'location':location, 
            'status_color':status['color'], 
            'status_label':status['label'], 
            'last_connection_human':last_connection['human'], 
            'last_connection_timestamp':last_connection['timestamp'], 
            
            'last_data_human':last_data['human'], 
            'last_data_timestamp':last_data['timestamp'], 
            
            'last_ssh_human':last_ssh['human'], 
            'last_ssh_timestamp':last_ssh['timestamp'], 
            
            'last_log_human':last_log['human'], 
            'last_log_timestamp':last_log['timestamp'], 
        })

    return render_template('nodes.html',
        show_all_nodes = bAllNodes,
        api_url = api_url,
        utc_now = dtUtcNow.strftime("%Y-%m-%d %H:%M:%S"),
        list_rows = listRows)



        
@web.route('/nodes/<node_id>/')
def web_node_page(node_id):
    logger.debug('GET web_node_page()  node_id = {}'.format(node_id))

    data = {}
    datesUnion = set()
    listDebug = []

    listDebug.append('''
        <head>
            <style>
                table {    border-collapse: collapse; }
                table, td, th { border: 1px solid black; padding: 1px 5px;}
            </style>
        </head>''')

    for version in export.dataset_versions:
        listDebug.append(' VERSION ' + version + '<br>\n')

        api_call            = '%s1/nodes/%s/dates?version=%s' % (api_url, node_id, version)

        nodes_dict = export.list_node_dates(version)
        logger.debug('///////////// nodes_dict(version = {}) = {}'.format(version, str(nodes_dict)))
        dates = {'data' : nodes_dict.get(node_id, list())}

        data[version] = dates['data']
        listDebug.append(' >>>>>>>>>VERSION ' + version + ' DATES: ' + str(dates)  + '<br>\n')
        datesUnion.update(data[version])     # union of all dates

    datesUnionSorted = sorted(list(datesUnion), reverse=True)

    dateList = []
    for date in datesUnionSorted:
        l = list()
        l.append(date)
        for version in export.dataset_versions:
            if date in data[version]:
                l.append('<a href="/api/1/nodes/%s/export?date=%s&version=%s">download</a>' % (node_id, date, version))
            else:
                l.append('')

        dateList.append(l)

    listDebug.append('dateList = ' + '<br><br>\n\n   {}'.format(str(dateList)))
    logger.debug('  DEBUG: ' + '\n'.join(listDebug))

    return render_template('node_data.html',
        node_id = node_id,
        web_host = web_host,
        api_call = api_call,
        api_url = api_url,
        dateList = dateList)

@web.route('/node/logs/<node_id>/')
def web_node_logs_page(node_id):
    logger.debug('GET web_node_logs_page()  node_id = {}'.format(node_id))

    txt = export.get_node_logs(node_id)
    if len(txt) > 0:
        txt = txt.split('\n')
    else:
        txt = [' *** No log data at this time ***']

    return render_template('node_logs.html',
        node_id = node_id,
        utc_now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        txt = txt,
        api_call = '/api/1/nodes/%s/logs' % (node_id)
    )
        
