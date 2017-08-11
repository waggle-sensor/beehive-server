#!/usr/bin/env python3
from . import api
from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from flask import stream_with_context
import logging
from waggle.logging import JournalHandler
from waggle.logging import SlackHandler
import os
import re
import sys
import time
sys.path.append("../..")
import export
sys.path.pop()

sys.path.append("..")
from waggle.protocol.utils.mysql import *


app = Flask(__name__)
app.logger.setLevel(logging.INFO)

logger = logging.getLogger('beehive-flask')
logger.setLevel(logging.INFO)

handler = JournalHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)
app.logger.addHandler(handler)

# Publish errors to Slack.
handler = SlackHandler('https://hooks.slack.com/services/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')
handler.setLevel(logging.ERROR)
logger.addHandler(handler)
app.logger.addHandler(handler)

port = 80
api_url_internal = 'http://localhost'
api_url = 'http://beehive1.mcs.anl.gov'

# modify /etc/hosts/: 127.0.0.1	localhost beehive1.mcs.anl.gov
STATUS_Bad_Request = 400  # A client error
STATUS_Unauthorized = 401
STATUS_Not_Found = 404
STATUS_Server_Error = 500


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code and status_code==STATUS_Server_Error:
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


@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def get_mysql_db():
    return Mysql(host="beehive-mysql",
                 user="waggle",
                 passwd="waggle",
                 db="waggle")


@api.route('/testing')
def api_testing():
    return 'this is a test'


@api.route('/')
def api_root():
    return 'This is the Waggle Beehive API Server.\n'


@api.route('/1/')
def api_version():
    return 'This is the Waggle Beehive API Server.\n'


@api.route('/1/epoch')
def api_epoch():
    return jsonify({
        'epoch': int(time.time())
    })
    
@api.route('/1/cassandra_time')
def api_get_cassandra_time():
    return jsonify(export.get_cassandra_time())


def NodeQuery(node_id_queried=None, bAllNodes=False):
    # if node_id_queried, then filter only that node, otherwise, query all nodes
    # if bAllNodes ('b' is for 'bool') is True, print all nodes, otherwise filter the active ones

    db = get_mysql_db()

    all_nodes = []

    # apply the appropriate WHERE clause - node_id_queried trumps bAllNodes
    if node_id_queried:
        whereClause = " WHERE node_id = '{}'".format(node_id_queried)
    elif not bAllNodes:
        whereClause = " WHERE opmode != 'testing'"
    else:
        whereClause = ""

    query = "SELECT node_id, hostname, groups, description, reverse_ssh_port, name, location, last_updated, opmode FROM nodes {}".format(whereClause)

    logger.debug(' query = ' + query)

    mysql_nodes_result = db.query_all(query)

    for result in mysql_nodes_result:
        node_id, hostname, groups, description, reverse_ssh_port, name, location, last_updated, opmode = result

        if not node_id:
            continue

        # cleanup formatting
        node_id = node_id.lower()

        all_nodes.append({
            'node_id': node_id,
            'groups': groups.split(),
            'opmode': opmode,
            'description': description or '',
            'reverse_ssh_port': reverse_ssh_port,
            'name': name or '',
            'location': location or '',
            'last_updated': last_updated
        })

    return {
        'data': dict((node['node_id'], node) for node in all_nodes)
    }

    # if bAllNodes and not node_id_queried:
    #     nodes_dict = export.list_node_dates()
    #
    #     for node_id in nodes_dict.keys():
    #         if not node_id in all_nodes:
    #             all_nodes[node_id]={}
    #
    # # for node_id in all_nodes.keys():
    # #     logger.debug("%s %s" % (node_id, type(node_id)))
    #
    # if node_id_queried:
    #     obj = {"data": all_nodes.get(node_id_queried, {})}
    # else:
    #     obj = {"data": all_nodes}
    #
    # return obj


@api.route('/1/nodes/')
def api_nodes():
    # if bAllNodes ('b' is for 'bool') is True, print all nodes, otherwise filter the active ones
    bAllNodes = request.args.get('all', 'false').lower() == 'true'

    logger.info("__ api_nodes()  bAllNodes = {}".format(str(bAllNodes)))

    return jsonify(NodeQuery(bAllNodes=bAllNodes))


@api.route('/1/nodes/<node_id>')
def api_nodes_single(node_id):
    node_id = node_id.lower()

    logger.info("__ api_nodes_single()  node_id = {}".format(node_id))

    return NodeQuery(node_id_queried = node_id)


@api.route('/nodes')
def nodes():
    if request.accept_mimetypes.best == 'text/csv':
        return nodes_csv()
    else:
        return nodes_json()


def nodes_json():
    return jsonify(list(filtered_nodes()))


def nodes_csv():
    fmt = '{id},{name},{description},{location},{port}\n'
    return Response((fmt.format(**node) for node in filtered_nodes()),
                    mimetype='text/csv')


def get_nodes():
    rows = get_mysql_db().query_all('SELECT node_id, name, description, location, reverse_ssh_port FROM nodes')

    for row in rows:
        yield {
            'id': row[0].lower().rjust(16, '0'),
            'name': row[1] or '',
            'description': row[2] or '',
            'location': row[3] or '',
            'port': row[4] or 0,
        }


def filtered_nodes():
    filters = [(field, re.compile(pattern, re.I))
               for field, pattern in request.args.items()]

    return filter(lambda node: all(pattern.search(node[field])
                                   for field, pattern in filters),
                  get_nodes())


@api.route('/1/nodes/<node_id>/dates')
def api_dates(node_id):
    node_id = node_id.lower()
    version = request.args.get('version', '1')

    logger.info("__ api_dates()  version = {}".format(version))

    nodes_dict = export.list_node_dates(version)

    if not node_id in nodes_dict:
        logger.debug("nodes_dict.keys(): " + ','.join([x for x in nodes_dict]))
        #logger.debug("nodes_dict: " + json.dumps(nodes_dict))
        raise InvalidUsage("node_id not found in nodes_dict: " + node_id, status_code=STATUS_Bad_Request)

    dates = nodes_dict[node_id]

    logger.debug("dates: " + str(dates))

    obj = {}
    obj['data'] = sorted(dates, reverse=True)

    return jsonify(obj)


@api.route('/datasets')
def get_datasets():
    version = request.args.get('version', '2raw')

    try:
        datasets = export.get_datasets(version)
    except KeyError:
        return 'invalid dataset version', 404

    return jsonify(datasets)


@api.route('/1/nodes/all_dates')
def api_all_dates():
    version = request.args.get('version', '1')
    sort_type = request.args.get('sort', 'desc').lower()[:3]

    logger.info("__ api_all_dates()  version = {}".format(version))

    nodes_dict = export.list_node_dates(version)

    bSortReverse = False if sort_type == 'asc' else True
    for node_id in sorted(nodes_dict):
        nodes_dict[node_id].sort(reverse = bSortReverse)

    obj = {}
    obj['data'] = nodes_dict

    return jsonify(obj)


@api.route('/1/nodes_last_data/')
def api_nodes_last_data():
    return jsonify(export.get_nodes_last_update_dict('data'))

@api.route('/1/nodes_last_log/')
def api_nodes_last_log():
    return jsonify(export.get_nodes_last_update_dict('log'))

@api.route('/1/nodes_last_ssh/')
def api_nodes_last_ssh():
    return jsonify(export.get_nodes_last_update_dict('ssh'))
    
@api.route('/1/nodes_offline/')
def api_nodes_offline():
    return jsonify(export.get_nodes_offline_dict())

@api.route('/1/nodes/<node_id>/logs')
def api_logs(node_id):
    logger.info("__ api_logs()  node_id = {}".format(node_id))
    return jsonify({"data" : export.get_node_logs(node_id)})


@api.route('/1/node_metrics_date')
def api_node_metrics_date():
    date = request.args.get('date')

    logger.info("__ api_node_metrics_date()  date = {}".format(str(date)))

    if not date:
        raise InvalidUsage("date is empty", status_code=STATUS_Not_Found)
    d = export.get_node_metrics_date_dict(date)
    logger.info("  __ api_node_metrics_date()  d = {}".format(str(d)))
    return jsonify({"data" : d})
    
@api.route('/1/nodes/<node_id>/export')
def api_export(node_id):
    date = request.args.get('date')
    version = request.args.get('version', '1')
    sort_type = request.args.get('sort', 'desc').lower()[:3]
    limit = request.args.get('limit', None)

    logger.info("__ api_export()  date = {}, version = {}  sort_type = {} ".format(str(date), str(version), sort_type))

    if not date:
        raise InvalidUsage("date is empty", status_code=STATUS_Not_Found)

    r = re.compile('\d{4}-\d{1,2}-\d{1,2}')

    if not r.match(date):
        raise InvalidUsage("date format not correct", status_code=STATUS_Not_Found)

    logger.info("accepted date: %s" %(date))

    def generate():
        for row in export.export_generator(node_id, date, False, ';', version=version, limit=limit):
            yield row + '\n'

    if sort_type in ['non', 'fal']:   # 'none', 'false'
        return Response(stream_with_context(generate()), mimetype='text/csv')
    else:
        l = list(generate())
        if sort_type == 'asc':
            l.sort()
        else:
            l.sort(reverse = True)
        return Response(stream_with_context(l), mimetype='text/csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
