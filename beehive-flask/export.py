from cassandra.cluster import Cluster
import logging
import os
import re
import sys
import time

sys.path.append("..")
from waggle.protocol.utils.mysql import *
sys.path.pop()

logger = logging.getLogger('beehive-api')

dataset_versions = ['2', '2raw', '1']   # These should match the keys in the dataset_version_table and be sorted in the same order as they appear in the columns on the node data pages
dataset_version_table = {
    '1': 'sensor_data',
    '2raw': 'sensor_data_raw',
    '2': 'sensor_data_decoded',
}


# NOTE This is ok, but it may be nicer to move this to an application /
# per-route / level decorator.
def retry(attempts=3, delay=1):
    def wrap(f):
        def wrapped(*args, **kwargs):
            exception = None
            for attempt in range(attempts):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    exception = e
                    time.sleep(delay * 2 ** min(attempt, 3))
            else:
                raise exception
        return wrapped
    return wrap


# NOTE Probably want connection to be cached and then more safely insert
# parameters into query.
@retry(attempts=5, delay=3)
def query(statement):
    logger.info('Connecting to Cassandra cluster.')
    cluster = Cluster(['beehive-cassandra'])

    logger.info('Connecting to Cassandra database.')
    session = cluster.connect('waggle')

    logger.info('Executing Cassandra query.  {}'.format(statement))
    rows = session.execute(statement)

    return cluster, rows


def get_mysql_db():
    return Mysql(host="beehive-mysql",
                 user="waggle",
                 passwd="waggle",
                 db="waggle")


def validate_node_id(node_id):
    """ returns (True,None) if the node_id is valid, 
        otherwise returns (False, msg) where msg is an error message
    """
    success = False
    msg = None
    
    if node_id and re.match('^[0-9a-fA-F]{16}$', node_id):
        success = True
    if not success:
        msg = "ERROR: Illegal node_id.  Must be 16 hexadecimal characters."
    return (success, msg)
    
def validate_version(version):
    """ returns (True,None) if the version is valid, 
        otherwise returns (False, msg) where msg is an error message
    """
    success = False
    msg = None
    
    if version and version in dataset_version_table.keys():
        success = True
    if not success:
        msg = "ERROR: Illegal version.  Must be one of {}.".format(str(dataset_version_table.keys()))
    return (success, msg)
    
def validate_date(theDate):
    """ returns (True,None) if theDate is a valid date, 
        otherwise returns (False, msg) where msg is an error message
    """
    success = False
    msg = None
    
    if theDate and re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', theDate):
        success = True
    if not success:
        msg = 'ERROR: Illegal date.  Must be in "YYYY-MM-DD" format.'
    return (success, msg)
    
                 
def export_generator(node_id, date, ttl, delimiter=';', version='1', limit = None):
    """
    Python generator to export sensor data from Cassandra
    version = 1 or 2 or 2.1, indicates which database/dataset is being queried
    """
    statement = None
    
    node_id = node_id.lower()
    # TODO check if node exists
    valid_node_id, msg = validate_node_id(node_id)
    if valid_node_id:
        valid_date, msg = validate_date(date)
        if valid_date:
            valid_version, msg = validate_version(version)
            if valid_version:
            
                limitString = ''
                if limit:
                    try:
                        limit_int = int(limit)
                        limitString = ' LIMIT {:d}'.format(limit_int)
                    except:
                        pass

                if version == '1':
                    statement = """SELECT node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data
                                FROM waggle.sensor_data
                                WHERE node_id='{}' AND date='{}' {}""".format(node_id, date, limitString)
                elif version == '2raw':  # 2 raw
                    statement = """SELECT node_id, date, ingest_id, plugin_name, plugin_version, plugin_instance, timestamp, parameter, data
                                FROM waggle.sensor_data_raw
                                WHERE node_id='{}' AND date='{}' {}""".format(node_id, date, limitString)
                elif version == '2':
                    statement = """SELECT node_id, date, ingest_id, meta_id, timestamp, data_set, sensor, parameter, data, unit
                                FROM waggle.sensor_data_decoded
                                WHERE node_id='{}' AND date='{}' {}""".format(node_id, date, limitString)

    if statement:
        cluster, rows = query(statement)

        count = 0

        if version == '1':
            for (node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data) in rows:
                count +=1
                #yield "%s,%s,%s,%s,%s,%s,%s,%s,%s" % (node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data)
                yield delimiter.join((node_id, date, plugin_id, str(plugin_version), plugin_instance, str(timestamp), sensor, sensor_meta, str(data)))
        elif version == '2raw':  # 2 raw
            for (node_id, date, ingest_id, plugin_name, plugin_version, plugin_instance, timestamp, parameter, data) in rows:
                count += 1
                # yield "%s,%s,%s,%s,%s,%s,%s,%s,%s" % (node_id, date, ingest_id, plugin_name, plugin_version, plugin_instance, timestamp, parameter, data)
                # yield delimiter.join((str(timestamp), str(ingest_id), plugin_name, plugin_version, plugin_instance, parameter, data))
                yield delimiter.join((str(timestamp), plugin_name, plugin_version, plugin_instance, parameter, data[2:-1]))
        else:  # version == 2
            for (node_id, date, ingest_id, meta_id, timestamp, data_set, sensor, parameter, data, unit) in rows:
                count += 1
                # yield "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (node_id, date, ingest_id, meta_id, timestamp, data_set, sensor, parameter, data, unit)
                yield delimiter.join((str(timestamp), data_set, sensor, parameter, data, unit))



def list_node_dates(version='1'):
    """
    Returns hash of nodes with dates.
    version = 1 or 2, indicates which database/dataset is being queried
    """
    try:
        table = dataset_version_table[version]
        statement = 'SELECT DISTINCT node_id, date FROM {}'.format(table)
    except KeyError:
        statement = None

    nodes = {}

    if statement:
        cluster, rows = query(statement)

        for (node_id, date) in rows:
            node_id = node_id.lower()

            if node_id not in nodes:
                nodes[node_id] = []

            nodes[node_id].append(date)

    return nodes


def get_datasets(version):
    try:
        table = dataset_version_table[version]
        statement = 'SELECT DISTINCT node_id, date FROM {}'.format(table)
    except KeyError:
        statement = None

    datasets = []
    if statement:
        cluster, rows = query(statement)

        for node_id, date in rows:
            datasets.append({
                'node_id': node_id.lower()[-12:],
                'date': date,
                'version': version,
                'url': 'http://beehive1.mcs.anl.gov/api/1/nodes/{}/export?date={}&version={}'.format(node_id, date, version),
            })

    return datasets


def get_nodes_last_update_dict(dataType = None):
    """
    Returns dictionary that maps node_id to the last_update of the specified data type.
    """
    dataTypes = ['data', 'log', 'ssh']
    if dataType in dataTypes:
        statement = "SELECT node_id, blobAsBigInt(last_update) FROM waggle.nodes_last_{}".format(dataType)
        cluster, rows = query(statement)
        result = dict((nodeid.lower(), timestamp) for nodeid, timestamp in rows)
    else:
        print('illegal dataType: {}; must be one of : {}'.format(dataType, str(dataTypes)))
        result = {}
        
    return result
    
def get_node_metrics_date_dict(date):
    """
    Returns dictionary of node-metrics data for a given date, the result is a dictionary with the structure:
       {timestamp : { node_id : { data } } }
    """
    d = {}

    valid_date, msg = validate_date(date)
    if valid_date:
        statement = "SELECT blobAsBigInt(timestamp), node_id, data FROM waggle.node_metrics_date WHERE date = '{}'".format(date)
        cluster, rows = query(statement)
        for row in rows:
            logger.info('   row = ', row)
            timestamp, node_id, data = row
            if timestamp not in d:
                d[timestamp] = {}
            if node_id not in d[timestamp]:
                d[timestamp][node_id] = [data]
            else:
                d[timestamp][node_id].append(data)
    return d

    

def get_nodes_offline_dict():
    """
    Returns dictionary that maps node_id to the start_time of OFFLINE state
    """
    all_nodes = {}

    query = "SELECT node_id, UNIX_TIMESTAMP(start_time) FROM waggle.node_offline"
    db = get_mysql_db()
    query_result = db.query_all(query)
    for result in query_result:
        node_id, start_time = result
        all_nodes[node_id] = start_time
    
    return all_nodes

    
def set_node_offline(node_id, bOffline = True):
    """ if bOffline == True, sets the offline entry for a single node to the current time
        if bOffline == False, clears the offline entry
    """
    valid_node_id, msg = validate_node_id(node_id)
    if valid_node_id:
        try:
            db = get_mysql_db()
            
            query = "DELETE FROM waggle.node_offline WHERE LOWER(node_id) = '{}';".format(node_id.lower())
            print('QUERY = ', query)
            for x in db.query_all(query):
                print(x)
            
            if bOffline:
                db.query_all("INSERT INTO waggle.node_offline (node_id) VALUES ('{}');".format(node_id))
        except:
            print('ERROR: operation failed!')


def get_nodes(bAllNodes = False):
    db = get_mysql_db()

    all_nodes = {}

    # limit the output with a WHERE clause if bAllNodes is false
    whereClause = " " if bAllNodes else " WHERE opmode = 'production' "

    query = "SELECT node_id, hostname, groups, description, reverse_ssh_port, name, location, last_updated, opmode FROM nodes {};".format(whereClause)

    logger.debug(' query = ' + query)

    mysql_nodes_result = db.query_all(query)

    for result in mysql_nodes_result:
        node_id, hostname, groups, description, reverse_ssh_port, name, location, last_updated, opmode = result

        if not node_id:
            continue

        # cleanup formatting
        node_id = node_id.lower()

        all_nodes[node_id] = {
            'node_id': node_id,
            'groups': groups.split(),
            'description': description,
            'reverse_ssh_port': reverse_ssh_port,
            'name': name,
            'location': location,
            'last_updated': last_updated,
            'opmode' : opmode
        }


    if bAllNodes:
        nodes_dict = list_node_dates()

        for node_id in nodes_dict.keys():
            if not node_id in all_nodes:
                all_nodes[node_id]={}

    return all_nodes

    
def get_node_logs(node_id):
    logger.info("__ export.get_node_logs()  node_id = {}".format(node_id))
    result = ''

    valid_node_id, msg = validate_node_id(node_id)
    if valid_node_id:
        maxBytes = 100000
        logFilePath = '/mnt/beehive/node-logs/'
        try:
            filename = logFilePath + node_id.strip().lower()
            logger.info('filename = "{}"'.format(filename))
            with open(filename, 'r') as f:
                f.seek(0, os.SEEK_END)        # end of file
                nBytes = f.tell()
                if nBytes > maxBytes:
                    f.seek(nBytes - maxBytes)
                    f.readline()    # seek ahead to the start of next line
                else:
                    f.seek(0)       # seek to start of file to read the whole thing
                result = f.read()
        except:
            pass
    return result

# This is just to test beehive-flask's connection to Cassandra - which often breaks    
def get_cassandra_time():
    statement = 'SELECT dateof(now()) FROM system.local ;'
    cluster, rows = query(statement)
    return rows[0][0]
    
