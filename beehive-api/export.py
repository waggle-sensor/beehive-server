#!/usr/bin/env python3

import logging, time, argparse, sys
from cassandra.cluster import Cluster

#start container:
#docker run -it --name=export -v ${DATA}/export:/export --link beehive-cassandra:cassandra --rm waggle/beehive-server /bin/bash


LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - line=%(lineno)d - %(message)s'
formatter = logging.Formatter(LOG_FORMAT)

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)

logger.addHandler(handler)

CASSANDRA_HOST="beehive-cassandra"

def query(statement):
    """
    Generic query function for Cassandra.
    Returns:
    cluster opbject. it is the callers responsibility to call cluster.shutdown()
    rows: result of the query
    """
    cluster = Cluster(contact_points=[CASSANDRA_HOST])
    session = None

    try_connect = 0
    while not session:
        try_connect += 1
        logger.info("try to connect to %s" % (CASSANDRA_HOST))
        try: # Might not immediately connect. That's fine. It'll try again if/when it needs to.
            session = cluster.connect('waggle')
        except:
            logger.warning("WARNING: Cassandra connection to " + CASSANDRA_HOST + " failed.")
            if try_connect >= 3:
                raise Exception("Error: 3 failed attempts to connect to cassandra.")
            else:
                logger.warning("The process will attempt to re-connect at a later time.")
        if not session:
            time.sleep(3)

    logger.debug("statement: %s" % (statement))
    try:
        rows = session.execute(statement)
    except Exception as e:
        logger.error("Could not execute statement: %s" % (str(e)))
        raise

    return cluster, rows

def export_generator(node_id, date, ttl, delimiter, version = '1'):
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

    try:
        cluster, rows = query(statement)
    except:
        raise

    if not delimiter:
        delimiter = ';'

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
            yield delimiter.join((str(timestamp), str(ingest_id), plugin_name, plugin_version, plugin_instance, parameter, data))
    else:  # version == 2
        for (node_id, date, ingest_id, meta_id, timestamp, data_set, sensor, parameter, data, unit) in rows:
            count += 1
            # yield "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (node_id, date, ingest_id, meta_id, timestamp, data_set, sensor, parameter, data, unit)
            yield delimiter.join((str(timestamp), data_set, sensor, parameter, data, unit))

    cluster.shutdown()
    logger.info("Retrieved %d rows" % (count))


def list_node_dates(version = '1'):
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

    nodes={}
    count = 0;
    for (node_id, date) in rows:
        node_id = node_id.lower()

        if not node_id in nodes:
            nodes[node_id]=[]
            count = count +1
        nodes[node_id].append(date)

    cluster.shutdown()
    logger.info("Found %d node_ids." % (count))
    return nodes

def get_nodes_last_update_dict():
    """
    Returns dictionary that maps node_id to last_update.
    Only works for version 2 data.
    """
    statement = "SELECT node_id, blobAsBigInt(last_update) FROM waggle.nodes_last_update;"

    try:
        cluster, rows = query(statement)
        print('cluster =', cluster)
        print('rows =', rows)
    except:
        raise

    d = {}
    for (node_id, timestamp) in rows:
        print('   node_id = ', node_id, ',  timestamp = ', timestamp)
        d[node_id.lower()] = timestamp

    print('d =', d)
    cluster.shutdown()

    return d


if __name__ == "__main__":
    node_id=None
    date=None

    parser = argparse.ArgumentParser()
    #parser.add_argument('--logging', dest='enable_logging', help='write to log files instead of stdout', action='store_true')
    parser.add_argument('--ttl', dest='ttl', help='export only ttl data (latest sensor data)', action='store_true')
    parser.add_argument('--node_id', dest='node_id', help='node_id')
    parser.add_argument('--date', dest='date', help='date (not needed with ttl), format: YYYY-MM-DD, e.g. 2016-01-21')


    args = parser.parse_args()

    if not args.node_id:
        logger.error("node_id not defined")
        parser.print_help()
        sys.exit(1)

    if (not args.ttl) and (not args.date):
        logger.error("neither ttl nor date provided")
        parser.print_help()
        sys.exit(1)


    for row in export_generator(args.node_id, args.date, args.ttl, ';'):
        print(row)
