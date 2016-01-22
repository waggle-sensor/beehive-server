#!/usr/bin/env python

import logging, time, argparse
from cassandra.cluster import Cluster


logger = logging.getLogger(__name__)

CASSANDRA_HOST="cassandra"

def export(node_id, date):
    cluster = Cluster(contact_points=[CASSANDRA_HOST])
    session = None

    while not session:
        print "try to connect"
        try: # Might not immediately connect. That's fine. It'll try again if/when it needs to.
            session = cluster.connect('waggle')
        except:
            logger.warning("WARNING: Cassandra connection to " + CASSANDRA_HOST + " failed.")
            logger.warning("The process will attempt to re-connect at a later time.")
        if not session:
            time.sleep(3)

    statement = "SELECT node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data FROM waggle.sensor_data_ttl WHERE node_id='%s' AND date='%s'" %(node_id, date)
    rows = session.execute(statement)


    for (node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data) in rows:
        print "%s,%s,%s,%s,%s,%s,%s,%s,%s" % (node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data)


if __name__ == "__main__":
    node_id=None
    date=None
    
    parser = argparse.ArgumentParser()
    #parser.add_argument('--logging', dest='enable_logging', help='write to log files instead of stdout', action='store_true')
    parser.add_argument('--node_id', dest='node_id', help='node_id', action='store_true')
    parser.add_argument('--date', dest='date', help='date, format: YYYY-MM-DD, e.g. 2016-01-21', action='store_true')
    
    
    args = parser.parse_args()
    
        
   

