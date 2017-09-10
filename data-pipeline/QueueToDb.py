#!/usr/bin/env python3
import os
import sys
import argparse
import binascii
from cassandra.cluster import Cluster
import datetime
import json
import logging
from multiprocessing import Process
import pika
import time
sys.path.append(os.path.abspath('../'))
sys.path.append("/usr/lib/waggle/")
sys.path.append("/usr/lib/waggle/beehive-server")
from config import *
from waggle_protocol.protocol.PacketHandler import *
from waggle_protocol.utilities.gPickler import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BEEHIVE_DEPLOYMENT = os.environ.get('BEEHIVE_DEPLOYMENT', '/')
CASSANDRA_HOST = 'beehive-cassandra'


class DataProcess(Process):

    def __init__(self, is_database_raw, verbosity=0):
        super(DataProcess, self).__init__()

        if is_database_raw:
            self.input_exchange = 'data-pipeline-in'
            self.queue = 'db-raw'
            self.statement = "INSERT INTO sensor_data_raw (node_id, date, plugin_name, plugin_version, plugin_instance, timestamp, parameter, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            self.function_ExtractValuesFromMessage = self.ExtractValuesFromMessage_raw
        else:
            self.input_exchange = 'plugins-out'
            self.queue = 'db-decoded'
            self.statement = "INSERT INTO sensor_data_decoded (node_id, date, ingest_id, meta_id, timestamp, data_set, sensor, parameter, data, unit) VALUES (?, ?, ?, ?, ?,   ?, ?, ?, ?, ?)"
            self.function_ExtractValuesFromMessage = self.ExtractValuesFromMessage_decoded

        logger.info("Initializing DataProcess")

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='beehive-rabbitmq',
            port=5672,
            virtual_host=BEEHIVE_DEPLOYMENT,
            credentials=pika.PlainCredentials(
                username='loader_raw',
                password='waggle',
            ),
            connection_attempts=10,
            retry_delay=3.0))

        self.verbosity = verbosity
        self.numInserted = 0
        self.numFailed = 0
        self.session = None
        self.cluster = None
        self.prepared_statement = None

        self.cassandra_connect()

        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        # Declare this process's queue
        self.channel.queue_declare(self.queue, durable=True)

        self.channel.queue_bind(
            exchange=self.input_exchange,
            queue=self.queue)

        try:
            self.channel.basic_consume(self.callback, queue=self.queue)
        except KeyboardInterrupt:
           logger.info("exiting.")
           sys.exit(0)
        except Exception as e:
           logger.error("error: %s" % (str(e)))

    def callback(self, ch, method, props, body):
        try:
            for iValues, values in enumerate(self.function_ExtractValuesFromMessage(props, body)):
                self.cassandra_insert(values)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            values = None
            self.numFailed += 1
            logger.error("Error inserting data: %s" % (str(e)))
            logger.error(' method = {}'.format(repr(method)))
            logger.error(' props  = {}'.format(repr(props)))
            logger.error(' body   = {}'.format(repr(body)))

            # TODO With this, we drop every failed message... I'm not sure if we want to do that...
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # Parse a message of sensor data and convert to the values to be inserted into a row in the db.  NOTE: this is a generator - because the decoded messages produce multiple rows of data.
    def ExtractValuesFromMessage_raw(self, props, body):
        versionStrings = props.app_id.split(':')
        sampleDatetime = datetime.datetime.utcfromtimestamp(float(props.timestamp) / 1000.0)
        sampleDate = sampleDatetime.strftime('%Y-%m-%d')
        # TODO Validate / santize node_id here.
        node_id = props.reply_to
        plugin_name = versionStrings[0]
        plugin_version = versionStrings[1]
        plugin_instance = '0' if (len(versionStrings) < 3) else versionStrings[2]
        timestamp = int(props.timestamp)
        parameter = props.type
        data = binascii.hexlify(body).decode()

        yield (node_id, sampleDate, plugin_name, plugin_version, plugin_instance, timestamp, parameter, data)

    def ExtractValuesFromMessage_decoded(self, props, body):
        dictData = json.loads(body.decode())

        # same for each parameter:value pair
        sampleDatetime = datetime.datetime.utcfromtimestamp(float(props.timestamp) / 1000.0)
        # TODO Validate / santize node_id here.
        node_id = props.reply_to
        sampleDate = sampleDatetime.strftime('%Y-%m-%d')
        ingest_id = 0
        meta_id = 0
        timestamp = int(props.timestamp)
        data_set = props.app_id
        sensor = props.type
        unit = 'NO_UNIT'

        for k in dictData.keys():
            parameter = k
            data = str(dictData[k])
            yield (node_id, sampleDate, ingest_id, meta_id, timestamp, data_set, sensor, parameter, data, unit)

    def cassandra_insert(self, values):

        if not self.session:
            self.cassandra_connect()

        if not self.prepared_statement:
            try:
                self.prepared_statement = self.session.prepare(self.statement)
            except Exception as e:
                logger.error("Error preparing statement: (%s) %s" % (type(e).__name__, str(e)) )
                raise

        bound_statement = self.prepared_statement.bind(values)

        connection_retry_delay = 1

        while True:
            # this is long term storage
            try:
                self.session.execute(bound_statement)
            except TypeError as e:
                 logger.error("QueueToDb: (TypeError) Error executing cassandra cql statement: %s -- values was: %s" % (str(e), str(values)) )
                 break
            except Exception as e:
                logger.error("QueueToDb: Error (type: %s) executing cassandra cql statement: %s -- values was: %s" % (type(e).__name__, str(e), str(values)) )
                if "TypeError" in str(e):
                    logger.debug("detected TypeError, will ignore this message")
                    break

                self.cassandra_connect()
                time.sleep(connection_retry_delay)
                if connection_retry_delay < 10:
                    connection_retry_delay += 1
                continue

            break

    def cassandra_connect(self):
        bDone = False
        iTry = 0
        while not bDone and (iTry < 5):
            if self.cluster:
                try:
                    self.cluster.shutdown()
                except:
                    pass

            self.cluster = Cluster(contact_points=[CASSANDRA_HOST])
            self.session = None

            iTry2 = 0
            while not bDone and (iTry2 < 5):
                iTry2 += 1
                try: # Might not immediately connect. That's fine. It'll try again if/when it needs to.
                    self.session = self.cluster.connect('waggle')
                    if self.session:
                        bDone = True
                except:
                    logger.warning("QueueToDb: WARNING: Cassandra connection to " + CASSANDRA_HOST + " failed.")
                    logger.warning("QueueToDb: The process will attempt to re-connect at a later time.")
                if not bDone:
                     time.sleep(3)

    def run(self):
        self.cassandra_connect()
        self.channel.start_consuming()

    def join(self):
        super(DataProcess,self).terminate()
        self.connection.close(0)
        if self.cluster:
            self.cluster.shutdown()


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('database', choices = ['raw', 'decoded'],
        help = 'which database the data is flowing to')
    argParser.add_argument('--verbose', '-v', action='count')
    args = argParser.parse_args()
    is_database_raw = args.database == 'raw'
    verbosity = 0 if not args.verbose else args.verbose

    p = DataProcess(is_database_raw, verbosity)
    p.start()

    print(__name__ + ': created process ', p)
    time.sleep(10)

    while p.is_alive():
        time.sleep(10)

    print(__name__ + ': process is dead, time to die')
    p.join()
