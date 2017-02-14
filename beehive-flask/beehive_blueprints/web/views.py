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
    ('year', datetime.timedelta(days = 365).total_seconds()),
    ('month', datetime.timedelta(days = 30).total_seconds()),
    ('week', datetime.timedelta(days = 7).total_seconds()),
    ('day', datetime.timedelta(days = 1).total_seconds()),
    ('hour', datetime.timedelta(seconds = 3600).total_seconds()),
    ('minute', datetime.timedelta(seconds = 60).total_seconds()),
]

def timedelta_to_human_readable(delta):
    s = '1 minute ago'
    delta_seconds = delta.total_seconds()

    for dur in durations_human_readable:
        if delta_seconds >= dur[1]:
            num = int(delta_seconds / dur[1])
            s = '{} {}{} ago'.format(num, dur[0], '' if num < 2 else 's')
            break
    return s

@web.route("/new")
def main_page_new():

    api_call = web_host + '/api/1/'

    # if bAllNodes ('b' is for 'bool') is True, print all nodes, otherwise filter the active ones
    bAllNodes = request.args.get('all', 'false').lower() == 'true'

    dtUtcNow = datetime.datetime.utcnow()

    # request last_update info
    lastUpdateTypes = ['data', 'log', 'ssh']
    dictLastUpdate = {t : export.get_nodes_last_update_dict(t) for t in lastUpdateTypes}
    dictLastUpdateData = dictLastUpdate['data']
    dictOffline = export.get_nodes_offline_dict()

    listRows = []

    all_nodes = export.get_nodes(bAllNodes)

    # header row
    headings = ['Vinyl Sticker Number', 'Node ID', 'Description', 'Location', 'Status', 'Last Connection', 'Last Data']
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
        # last_data contains its own <td> and </td> because it modifies them for color
        # eg. <td style="background-color:#FF0000">
        last_data = '<td></td>'
        duration_string = ''

        if node_id in dictLastUpdateData:
            dt = datetime.datetime.utcfromtimestamp(float(dictLastUpdateData[node_id])/1000.0)
            #s = dt.isoformat(sep = ' ')
            s = dt.strftime("%Y-%m-%d %H:%M:%S")
            delta = dtUtcNow - dt
            if bAllNodes:
                color = timeToColors[-1][1] # negative time - should correspond to last value
                for tuple in timeToColors:
                    if delta > tuple[0]:
                        color = tuple[1]
                        break
            else:
                color = '#ffffff'

            # human-readable duration
            duration_string = timedelta_to_human_readable(delta)
            last_data = '<td align="left" style="background-color:{}"><b>{}</b> <tt>({})</tt></td>'.format(color, duration_string, s)

        status = "S'all good"
        listRows.append('''<tr>
            <td align="right"><tt>%s</tt></td>
            <td><a href="%snodes/%s"><tt>%s</tt></a></td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            %s
            </tr>'''                \
            % (name, web_host, node_id, node_id, description, location, status, last_data, last_data))

    return render_template('nodes.html',
        api_url = api_url,
        utc_now = dtUtcNow.strftime("%Y-%m-%d %H:%M:%S"),
        list_rows = listRows)


        

@web.route("/")
def main_page():

    api_call = web_host + '/api/1/'

    # if bAllNodes ('b' is for 'bool') is True, print all nodes, otherwise filter the active ones
    bAllNodes = request.args.get('all', 'false').lower() == 'true'

    dtUtcNow = datetime.datetime.utcnow()

    # request last_update
    dictLastUpdate = export.get_nodes_last_update_dict('data')

    listRows = []

    all_nodes = export.get_nodes(bAllNodes)

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
            if bAllNodes:
                color = timeToColors[-1][1] # negative time - should correspond to last value
                for tuple in timeToColors:
                    if delta > tuple[0]:
                        color = tuple[1]
                        break
            else:
                color = '#ffffff'

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
            <td><a href="%snodes/%s"><tt>%s</tt></a></td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            %s
            </tr>'''                \
            % (name, web_host, node_id, node_id, description, hostname, location, last_updated))

    return render_template('nodes.html',
        api_url = api_url,
        utc_now = dtUtcNow.strftime("%Y-%m-%d %H:%M:%S"),
        list_rows = listRows)
        
        
@web.route('/nodes/<node_id>/')
def web_node_page(node_id):
    logger.debug('GET web_node_page()  node_id = {}'.format(node_id))

    versions = ['2', '2raw', '1']
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

    for version in versions:
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
        for version in versions:
            if date in data[version]:
                l.append('<a href="%s1/nodes/%s/export?date=%s&version=%s">download</a>' % (api_url, node_id, date, version))
            else:
                l.append('')

        dateList.append(l)

    listDebug.append('dateList = ' + '<br><br>\n\n   {}'.format(str(dateList)))
    logger.debug('  DEBUG: ' + '\n'.join(listDebug))

    return render_template('node_data.html',
        node_id = node_id,
        api_call = api_call,
        api_url = api_url,
        dateList = dateList)
