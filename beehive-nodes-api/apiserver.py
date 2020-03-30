#!/usr/bin/env python3
import logging
import os.path
import re
import sys
import json
import time
import requests
#from export import export_generator, list_node_dates, get_nodes_last_update_dict
#sys.path.append("..")
#from waggle_protocol.utilities.mysql import *
from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from flask import stream_with_context
#import mysqlclient
#from MySQLdb import _mysql
import MySQLdb as _mysql

app = Flask(__name__)
#app.logger.setLevel(logging.INFO)

logger = logging.getLogger('beehive-api')
logger.setLevel(logging.INFO)

#handler = JournalHandler()
#handler.setLevel(logging.INFO)
#logger.addHandler(handler)
#app.logger.addHandler(handler)

# Publish errors to Slack.
#handler = SlackHandler('https://hooks.slack.com/services/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')
#handler.setLevel(logging.ERROR)
#logger.addHandler(handler)
#app.logger.addHandler(handler)

port = 80
api_url_internal = 'http://localhost'
api_url = 'http://beehive1.mcs.anl.gov'

# modify /etc/hosts/: 127.0.0.1	localhost beehive1.mcs.anl.gov
STATUS_Bad_Request = 400  # A client error
STATUS_Unauthorized = 401
STATUS_Not_Found = 404
STATUS_Server_Error = 500


stat_dir = '/stats'

netstat_file = os.path.join(stat_dir , 'beehive-sshd-netstat.txt')
rmq_file = os.path.join(stat_dir , 'beehive-rabbitmq-list_connections_user.txt')
beehive_loader_raw_file = os.path.join(stat_dir , 'beehive-loader-raw.txt')
beehive_data_loader_file = os.path.join(stat_dir , 'beehive-data-loader.txt')



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


def get_mysql_db():
    host = os.environ.get("MYSQL_HOST")
    user = os.environ.get("MYSQL_USER")
    passwd = os.environ.get("MYSQL_PASSWD")
    db = os.environ.get("MYSQL_DB")

    return _mysql.connect(host=host, user=user, passwd=passwd,db=db)
  

#@app.route('/api/')
#def api_root():
#    return 'This is the beehive API server.'


#@app.route('/api/1/')
#def api_version():
#    return 'This is the beehive API server.'


#@app.route('/api/1/epoch')
#def api_epoch():
#    return jsonify({
#        'epoch': int(time.time())
#    })


#example: node_id,vsn,rssh_port,opmode,project,description,location,iccid,imei
# vsn=name, rssh_port=reverse_ssh_port, 

# reproduce with filter=node_id,name,reverse_ssh_port,opmode,project,description,location,iccid,imei
# http://localhost:8183/api/1/nodes/?format=node_id,name,reverse_ssh_port,opmode,project,description,location,iccid,imei
# http://localhost:8183/api/1/nodes/?filter=node_id,name,reverse_ssh_port,opmode,project,description,location,iccid,imei&format=csv

#  available: id , node_id | project | description | reverse_ssh_port | hostname | hardware | name | location | last_updated | opmode | groups | iccid | imei | lon | lat






@app.route('/')
def api_nodes():

    return_obj = {}


    version = request.args.get('version', '1')
    # if bAllNodes ('b' is for 'bool') is True, print all nodes, otherwise filter the active ones
    #bAllNodes = request.args.get('all', 'false').lower() == 'true'

    #logger.info("__ api_nodes()  version = {}, bAllNodes = {}".format(
    #    version, str(bAllNodes)))

    table_fields = {"node_id", "hostname", "project", "description", "reverse_ssh_port", "name", "location", "last_updated"}

    other_fields = {"rssh_connection", "rmq_connection", "data_frames"}

    all_valid_fields = table_fields.union(other_fields)

    default_view = ["node_id", "hostname", "project", "description", "reverse_ssh_port", "name", "location", "last_updated"]
    #default_view = "node_id, hostname, project, description, reverse_ssh_port, name, location, last_updated"
    column_view = default_view

    filter = request.args.get('filter')

    if filter:
        custom_view = filter.split(',')
        column_view = custom_view

    for field in column_view:
        if not field in all_valid_fields:
            return_obj['error'] = "field {} not a valid field".format(field)
            return jsonify(return_obj), STATUS_Server_Error

    rssh_connection_view_index=-1
    try:
        rssh_connection_view_index = column_view.index('rssh_connection')
    except ValueError:
        rssh_connection_view_index=-1
    

    rmq_connection_view_index=-1
    try:
        rmq_connection_view_index = column_view.index('rmq_connection')
    except ValueError:
        rmq_connection_view_index=-1


    data_frames_view_index=-1
    try:
        data_frames_view_index = column_view.index('data_frames')
    except ValueError:
        data_frames_view_index=-1


    # get port information
    ports = set()
    if rssh_connection_view_index >= 0:
        
        with open(netstat_file) as fp:
            for line in fp:
                portInt=int(line.strip())
                ports.add(portInt)

        print('ports')
        print(ports)
        #return jsonify(str(ports))


    # get rmq_connection information

    data_frames_by_node={}
    if rmq_connection_view_index >= 0 or data_frames_view_index >=0 :
        
        #old_node_ids = set()
        with open(beehive_loader_raw_file) as fp:
            for line in fp:
                node_id = line.split(' ')[0].lower()
                if len(node_id) == 12:
                    node_id = "0000"+node_id
                #old_node_ids.add(node_id)
                if node_id in data_frames_by_node:
                    data_frames_by_node[node_id]+=1
                else:
                    data_frames_by_node[node_id]=1
        
        #new_node_ids=set()
        with open(beehive_data_loader_file) as fp:
            for line in fp:
                #print(line)
                node_id = line.strip().lower()[-12:]
                if len(node_id) == 12:
                    node_id = "0000"+node_id
                #new_node_ids.add(node_id)
                if node_id in data_frames_by_node:
                    data_frames_by_node[node_id]+=1
                else:
                    data_frames_by_node[node_id]=1


    print("\ndata_frames_by_node", flush=True)
    print(data_frames_by_node, flush=True)        


        #nodes_with_data_frames = old_node_ids.union(new_node_ids)
        # not clear to me what data_frames is, seems a boolean like rmq_connection
        #for node_id in nodes.keys():
        #    has_data_frames = node_id in data_frames
        #    nodes[node_id]['data_frames'] = has_data_frames
        #    if has_data_frames:
        #        nodes[node_id]['rmq_connection'] = True






    db_query_fields = [x for x in column_view if x in table_fields]
    if not 'rssh_connection':
        db_query_fields.append('rssh_connection')


    if not 'node_id':
        db_query_fields.append('node_id')

    #rssh_connection_query_index = db_query_fields.index('rssh_connection')
    #reverse_ssh_port_index=-1
    #try:
    #    reverse_ssh_port_index = db_query_fields.index('reverse_ssh_port')
    #except ValueError:
    #    reverse_ssh_port_index=-1


    out_format = request.args.get('format')
    
    if not out_format:
        out_format = "json"

    if not out_format in ["json", "csv"]:
        return 'format not supported', STATUS_Server_Error

    #if out_format:
    #    if out_format == "csv"

    db = get_mysql_db()

    all_nodes = []

    # limit the output with a WHERE clause if bAllNodes is false
    #whereClause = " " if bAllNodes else " WHERE opmode = 'active' "
    

    query = "SELECT {} FROM nodes ;".format(', '.join(db_query_fields))

    logger.debug(' query = ' + query)

    c=db.cursor()

    try:
        c.execute(query)

     # mysql_nodes_result = db.query_all(query)
        mysql_nodes_result = c.fetchall()

    #except _mysql.Error as e:
    except Exception as e:
    #except MySQLdb.Error as e: #MySQLdb.Warning
        try:
            error_message = "MySQL Error [{}]: {}".format(e.args[0], e.args[1])
            print(error_message)
            return_obj['error'] = error_message
            return jsonify(return_obj), STATUS_Server_Error
        except IndexError:
            error_message = "MySQL Error: {}".format(str(e))
            print(error_message)
            return_obj['error'] = error_message
            return jsonify(return_obj), STATUS_Server_Error

    result_csv = ""

    if out_format == "csv":
        # csv header line
        result_csv += ",".join(column_view) + "\n"

    for result in mysql_nodes_result:
        #node_id, hostname, project, description, reverse_ssh_port, name, location, last_updated = result

        if not result:
            continue

        # replace None
        #result = ['None' if v is None else v for v in result]
        

        #result_array = map(json.dumps, result_array) 

        # cleanup formatting
        #node_id = node_id.lower()

        
      
        # convert mysql results into object
        node_object = {}

        for i, field in enumerate(db_query_fields):
            node_object[field] = result[i]


        if not 'node_id' in node_object:
            return_obj['error'] = "node_id field missing in results"
            return jsonify(return_obj), STATUS_Server_Error

        nodeid = node_object['node_id']
        nodeid_lower = nodeid.lower()
        
        # add info about open port
        if rssh_connection_view_index >= 0:
            node_object['rssh_connection'] = False 
            if 'reverse_ssh_port' in node_object:
                reverse_ssh_port = node_object['reverse_ssh_port']
                # check if reverse_ssh_port is in the list of open ports
                if reverse_ssh_port in ports:
                    node_object['rssh_connection'] =  True

        

        if rmq_connection_view_index >= 0:
            had_rmq_connection = nodeid_lower in data_frames_by_node
            node_object['rmq_connection'] = had_rmq_connection
        
        if data_frames_view_index >= 0:
            if nodeid_lower in data_frames_by_node:
                node_object['data_frames'] = data_frames_by_node[nodeid_lower]
            else:
                node_object['data_frames'] = 0
        
        #print(result)
        if out_format == "csv":
            result_array = []
            
            for field in column_view:
                if field in node_object:
                    result_array.append(json.dumps(node_object[field]))
                else:
                    result_array.append("N/A")


            result_csv += ",".join(result_array)+"\n"

        

        if out_format == "json": 
     
            all_nodes.append(node_object)



    if out_format == "csv":
        return Response(result_csv, mimetype='text/csv')
       # return result_csv

    
    return_obj['data'] = all_nodes
    return jsonify(return_obj)
#     # return  json.dumps(obj, indent=4)


@app.route('/api/nodes')
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


# @app.route('/api/1/nodes/<node_id>/dates')
# def api_dates(node_id):
#     node_id = node_id.lower()
#     version = request.args.get('version', '1')

#     logger.info("__ api_dates()  version = {}".format(version))

#     nodes_dict = list_node_dates(version)

#     if not node_id in nodes_dict:
#         logger.debug("nodes_dict.keys(): " + ','.join([x for x in nodes_dict]))
#         #logger.debug("nodes_dict: " + json.dumps(nodes_dict))
#         raise InvalidUsage("node_id not found in nodes_dict: " + node_id, status_code=STATUS_Bad_Request)

#     dates = nodes_dict[node_id]

#     logger.debug("dates: " + str(dates))

#     obj = {}
#     obj['data'] = sorted(dates, reverse=True)

#     return jsonify(obj)


# @app.route('/api/nodes/<nodeid>/dates')
# def api_dates_v2(nodeid):
#     nodeid = nodeid.lower()
#     dates = list_node_dates(version='2')

#     try:
#         return jsonify(sorted(dates[nodeid], reverse=True))
#     except KeyError:
#         return 'node not found', 404


# @app.route('/api/1/nodes_last_update/')
# def api_nodes_last_update():
#     return jsonify(get_nodes_last_update_dict())


#@app.route('/api/1/nodes/<node_id>/export')
#def api_export(node_id):
#    date = request.args.get('date')
#    version = request.args.get('version', '1')

#    logger.info("__ api_export()  date = {}, version = {}".format(str(date), str(version)))

 #   if not date:
#        raise InvalidUsage("date is empty", status_code=STATUS_Not_Found)

#    r = re.compile('\d{4}-\d{1,2}-\d{1,2}')

#    if not r.match(date):
#        raise InvalidUsage("date format not correct", status_code=STATUS_Not_Found)

 #   logger.info("accepted date: %s" %(date))

#    def generate():
 #       for row in export_generator(node_id, date, False, ';', version=version):
 #           yield row + '\n'

 #   return Response(stream_with_context(generate()), mimetype='text/csv')


# @app.route('/api/1/WCC_node/<node_id>/')
# def WCC_web_node_page(node_id):
#     logger.debug('GET WCC_web_node_page()  node_id = {}'.format(node_id))

#     versions = ['2', '2.1', '1']
#     data = {}
#     datesUnion = set()
#     listDebug = []

#     for version in versions:
#         listDebug.append(' VERSION ' + version + '<br>\n')

#         api_call            = '%s/api/1/nodes/%s/dates?version=%s' % (api_url, node_id, version)
#         api_call_internal   = '%s/api/1/nodes/%s/dates?version=%s' % (api_url_internal, node_id, version)
#         logger.debug('     in WCC_web_node_page: api_call_internal = {}'.format(api_call_internal))

#         if False:
#             try:
#                 req = requests.get( api_url_internal ) # , auth=('user', 'password')
#             except Exception as e:
#                 msg = "Could not make request: %s", (str(e))
#                 logger.error(msg)
#                 continue
#                 #raise internalerror(msg)

#             if req.status_code != 200:
#                 msg = "status code: %d" % (req.status_code)
#                 logger.error(msg)
#                 continue
#                 #raise internalerror(msg)

#             try:
#                 dates = req.json()
#             except ValueError:
#                 logger.debug("Not json: " + str(req))
#                 continue
#                 #raise internalerror("not found")

#             if not 'data' in dates:
#                 logger.debug("data field not found")
#                 continue
#                 #raise internalerror("not found")
#         else:
#             nodes_dict = list_node_dates(version)
#             logger.debug('///////////// nodes_dict(version = {}) = {}'.format(version, str(nodes_dict)))
#             dates = {'data' : nodes_dict.get(node_id, list())}

#         data[version] = dates['data']
#         listDebug.append(' >>>>>>>>>VERSION ' + version + ' DATES: ' + str(dates)  + '<br>\n')
#         datesUnion.update(data[version])     # union of all dates

#     datesUnionSorted = sorted(list(datesUnion), reverse=True)

#     dateDict = {}
#     for date in datesUnionSorted:
#         l = list()
#         for version in versions:
#             if date in data[version]:
#                 l.append(date)
#             else:
#                 l.append('')
#         dateDict[date] = l

#     listDebug.append('<br><br>\n\n   {}'.format(str(dateDict)))
#     logger.debug('  DEBUG: ' + '\n'.join(listDebug))

#     return '<br>\n'.join(listDebug)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
