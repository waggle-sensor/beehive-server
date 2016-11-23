import logging
from cassandra.cluster import Cluster
import time


logger = logging.getLogger('beehive-api')


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

    logger.info('Executing Cassandra query.')
    rows = session.execute(statement)

    return cluster, rows


def export_generator(node_id, date, ttl, delimiter=';', version='1'):
    """
    Python generator to export sensor data from Cassandra
    version = 1 or 2 or 2.1, indicates which database/dataset is being queried
    """
    node_id = node_id.lower()
    # TODO check if node exists

    if version == '1':
        statement = "SELECT node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data "+ \
                    "FROM waggle.sensor_data "+ \
                    "WHERE node_id='%s' AND date='%s'" %(node_id, date)
    elif version == '2.1':  # 2 raw
        statement = "SELECT node_id, date, ingest_id, plugin_name, plugin_version, plugin_instance, timestamp, parameter, data "+ \
                    "FROM waggle.sensor_data_raw "+ \
                    "WHERE node_id='%s' AND date='%s'" %(node_id, date)
    else:   # version == 2
        statement = "SELECT node_id, date, ingest_id, meta_id, timestamp, data_set, sensor, parameter, data, unit "+ \
                    "FROM waggle.sensor_data_decoded "+ \
                    "WHERE node_id='%s' AND date='%s'" %(node_id, date)

    cluster, rows = query(statement)

    count = 0

    if version == '1':
        for (node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data) in rows:
            count +=1
            #yield "%s,%s,%s,%s,%s,%s,%s,%s,%s" % (node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data)
            yield delimiter.join((node_id, date, plugin_id, str(plugin_version), plugin_instance, str(timestamp), sensor, sensor_meta, str(data)))
    elif version == '2.1':  # 2 raw
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
    if version == '1':
        statement = "SELECT DISTINCT node_id,date FROM sensor_data"
    elif version == '2.1':
        statement = "SELECT DISTINCT node_id,date FROM sensor_data_raw"
    else:  # 2.0
        statement = "SELECT DISTINCT node_id,date FROM sensor_data_decoded"

    try:
        cluster, rows = query(statement)
    except:
        raise

    nodes = {}
    count = 0
    for (node_id, date) in rows:
        node_id = node_id.lower()

        if not node_id in nodes:
            nodes[node_id]=[]
            count = count +1
        nodes[node_id].append(date)

    return nodes


def get_nodes_last_update_dict():
    """
    Returns dictionary that maps node_id to last_update.
    Only works for version 2 data.
    """
    statement = "SELECT node_id, blobAsBigInt(last_update) FROM waggle.nodes_last_update"
    cluster, rows = query(statement)
    return dict((nodeid.lower(), timestamp) for nodeid, timestamp in rows)
