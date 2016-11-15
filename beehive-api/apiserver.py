#!/usr/bin/env python3
import os.path
import logging
import re
import sys
import json
import time
from export import export_generator, list_node_dates, get_nodes_last_update_dict
sys.path.append("..")
from waggle_protocol.utilities.mysql import *

from flask import Flask
app = Flask(__name__)
from flask import Response
from flask import request
from flask import jsonify
from flask import stream_with_context


# a production container
# docker run -it --name=beehive-api --net beehive --rm -p 8183:5000 waggle/beehive-api


# testing setup
# docker run -it --rm --name=beehive-api-test --net beehive -p 8184:5000 waggle/beehive-api-test


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


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def internalerror(e):
    message = html_header("Error") + "Sorry, there was an error:<br>\n<pre>\n"+str(e) +"</pre>\n"+ html_footer()
    return message


def get_mysql_db():
    return Mysql(host="beehive-mysql",
                 user="waggle",
                 passwd="waggle",
                 db="waggle")


@app.route('/api/')
def api_root():
    return 'This is the beehive API server.'


@app.route('/api/1/')
def api_version():
    return 'This is the beehive API server.'


@app.route('/api/1/epoch')
def api_epoch():
    return jsonify({
        'epoch': int(time.time())
    })

@app.route('/api/1/nodes/')
def api_nodes():

    version = request.args.get('version', '1')
    # if bAllNodes ('b' is for 'bool') is True, print all nodes, otherwise filter the active ones
    bAllNodes = request.args.get('all', 'false').lower() == 'true'
    
    logger.info("__ api_nodes()  version = {}, bAllNodes = {}".format(
        version, str(bAllNodes)))

    db = get_mysql_db()

    all_nodes = {}

    # limit the output with a WHERE clause if bAllNodes is false
    whereClause = " " if bAllNodes else " WHERE opmode = 'active' " 

    query = "SELECT node_id, hostname, project, description, reverse_ssh_port, name, location, last_updated FROM nodes {};".format(whereClause)
    
    logger.debug(' query = ' + query)   
    
    mysql_nodes_result = db.query_all(query)
    
    for result in mysql_nodes_result:
        node_id, hostname, project, description, reverse_ssh_port, name, location, last_updated = result

        if not node_id:
            continue

        # cleanup formatting
        node_id = node_id.lower()

        all_nodes[node_id] = {
            'project': project,
            'description': description,
            'reverse_ssh_port': reverse_ssh_port,
            'name': name,
            'location': location,
            'last_updated': last_updated
        }

    if bAllNodes:           # WCC: commenting this out
        nodes_dict = list_node_dates()

        for node_id in nodes_dict.keys():
            if not node_id in all_nodes:
                all_nodes[node_id]={}

    #for node_id in all_nodes.keys():
    #    logger.debug("%s %s" % (node_id, type(node_id)))

    obj = {}
    obj['data'] = all_nodes
    return jsonify(obj)
    #return  json.dumps(obj, indent=4)


@app.route('/api/2/nodes.json')
def nodes_json():
    db = get_mysql_db()
    rows = db.query_all('SELECT node_id, name, description, location, reverse_ssh_port FROM nodes')

    results = []

    filters = [(field, re.compile(pattern, re.I)) for field, pattern in request.args.items()]

    for row in rows:
        result = {
            'id': row[0].lower()[4:] or '',
            'name': row[1] or '',
            'description': row[2] or '',
            'location': row[3] or '',
            'port': row[4] or 0,
        }

        if all(pattern.search(result[field]) for field, pattern in filters):
            results.append(result)

    return jsonify(results)


@app.route('/api/2/nodes.csv')
def nodes_csv():
    db = get_mysql_db()
    rows = db.query_all('SELECT node_id, name, description, location, reverse_ssh_port FROM nodes')

    def stream():
        for row in rows:
            node = row[0].lower()[4:]
            name = row[1] or ''
            description = row[2] or ''
            location = row[3] or ''
            ssh_port = row[4] or ''
            yield '{},"{}","{}","{}",{}\n'.format(node, name, description, location, ssh_port)

    return Response(stream(), mimetype='text/csv')

@app.route('/api/1/nodes/<node_id>/dates')
def api_dates(node_id):
    node_id = node_id.lower()
    version = request.args.get('version', '1')

    logger.info("__ api_dates()  version = {}".format(version))
    
    nodes_dict = list_node_dates(version)

    if not node_id in nodes_dict:
        logger.debug("nodes_dict.keys(): " + ','.join([x for x in nodes_dict]))
        #logger.debug("nodes_dict: " + json.dumps(nodes_dict))
        raise InvalidUsage("node_id not found in nodes_dict: " + node_id,  status_code=STATUS_Bad_Request )

    dates = nodes_dict[node_id]

    logger.debug("dates: " + str(dates))

    obj = {}
    obj['data'] = sorted(dates, reverse=True)

    return jsonify(obj)

@app.route('/api/1/nodes_last_update/')
def api_nodes_last_update():
    nodes_last_update_dict = get_nodes_last_update_dict()
    return jsonify(nodes_last_update_dict)

@app.route('/api/1/nodes/<node_id>/export')
def api_export(node_id):
    date = request.args.get('date')
    version = request.args.get('version', '1')

    logger.info("__ api_export()  date = {}, version = {}".format(str(date), str(version)))

    if not date:
        raise InvalidUsage("date is empty", status_code=STATUS_Not_Found)

    r = re.compile('\d{4}-\d{1,2}-\d{1,2}')

    if not r.match(date):
        raise InvalidUsage("date format not correct", status_code=STATUS_Not_Found)

    logger.info("accepted date: %s" %(date))

    def generate():
        for row in export_generator(node_id, date, False, ';', version=version):
            yield row + '\n'

    return Response(stream_with_context(generate()), mimetype='text/csv')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
