#!/usr/bin/env python3

# dataprocess.py

import sys
sys.path.append("..")
sys.path.append("/usr/lib/waggle/")
from multiprocessing import Process, Manager
from config import *
import pika
from waggle_protocol.protocol.PacketHandler import *
from waggle_protocol.utilities.gPickler import *
import logging, datetime, time
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
from cassandra.cqlengine.columns import Ascii
from cassandra.cqlengine.usertype import UserType



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DataProcess(Process):
    """
        This process handles all data submissions
    """

    def __init__(self):
        """
            Starts up the Data handling Process
        """
        super(DataProcess,self).__init__()
        
        logger.info("Initializing DataProcess")
        
        # Set up the Rabbit connection
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        #Connect to rabbitMQ
        while True:
            try:
                self.connection = pika.BlockingConnection(pika_params)
            except Exception as e:
                logger.error("QueueToRawDb: Could not connect to RabbitMQ server \"%s\": %s" % (pika_params.host, e))
                time.sleep(1)
                continue
            break
            
    
        logger.info("Connected to RabbitMQ server \"%s\"" % (pika_params.host))
        self.numInserted = 0
        self.session = None
        self.cluster = None
        self.prepared_statement = None
        
        self.cassandra_connect()
        
        
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        # Declare this process's queue
        self.channel.queue_declare("db-raw")
        
        self.channel.queue_bind(exchange = 'data-pipeline-in',
            queue = 'db-raw')
        
        try: 
            self.channel.basic_consume(self.callback, queue='db-raw')
        except KeyboardInterrupt:
           logger.info("exiting.")
           sys.exit(0)
        except Exception as e:
           logger.error("error: %s" % (str(e)))

    def callback(self, ch, method, props, body):
        #TODO: this simply drops failed messages, might find a better solution!? Keeping them has the risk of spamming RabbitMQ
        print('######################################')
        print('method = ', method)
        print('props = ', props)
        print('body = ', body)
        try:
            # if a field is mandatory, directly try to reference it - which will cause an exception
            # and prevent insertion if it fails;  Otherwise, use "get" with a default value.
            '''props =  <BasicProperties(['app_id=coresense:3', 'content_type=b', 'delivery_mode=2', 'reply_to=0000001e06107d97', 'timestamp=1476135836151', 'type=frame'])>
            '''
            versionStrings  = props.app_id.split(':')
            print('versionStrings: ', versionStrings)
            sampleDatetime  = datetime.utcfromtimestamp(props.timestamp)
            print('sampleDatetime: ', sampleDatetime)

            sampleDate      = sampleDatetime.strftime('%Y-%m-%d')
            print('sampleDate: ', sampleDate)

            node_id         = props.reply_to
            print('node_id: ', node_id)

            #ingest_id       = props.ingest_id ##props.get('ingest_id', 0)
            print('ingest_id: ', ingest_id)
            plugin_name     = versionStrings[0]
            plugin_version  = versionStrings[1]
            plugin_instance = 0 if len(versionStrings < 3) else versionStrings[2]
            print('plugin_name, plugin_version, plugin_instance : ', plugin_name, plugin_version, plugin_instance)
            timestamp       = int(props.timestamp)
            print('timestamp: ', timestamp)
            parameter       = props.type
            print('parameter: ', parameter)
            data            = body

            print('   node_id = ',          node_id         )
            print('   date = ',             sampleDate      )
            print('   ingest_id = ',        ingest_id       )
            print('   plugin_name = ',      plugin_name     )
            print('   plugin_version = ',   plugin_version  )
            print('   plugin_instance = ',  plugin_instance )
            print('   timestamp = ',        timestamp       )
            print('   parameter = ',        parameter       )
            print('   data = ',             data            )
        except:
            print('ERROR computing data for insertion into database')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        try:
            header, opt, data = unpack(body)
        except Exception as e:    
            logger.error("QueueToRawDb: Error unpacking data: %s" % (str(e)))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            #time.sleep(1)
            #self.cassandra_connect()#TODO I don't know if this is neccessary
            return
            
        try:    
            data = un_gPickle(data)
        except Exception as e:    
            logger.error("QueueToRawDb: Error un_gPickle data: %s" % (str(e)))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            #time.sleep(1)
            #self.cassandra_connect()#TODO I don't know if this is neccessary
            return

        if True:
            print("Data: ", data)
        else:
            try:
                print("Data: ", data)
                # Send the data off to Cassandra
                self.cassandra_insert(header,data)
            except Exception as e:    
                logger.error("QueueToRawDb: Error inserting data: %s" % (str(e)))
                ch.basic_ack(delivery_tag=method.delivery_tag)
                #time.sleep(1)
                #self.cassandra_connect()#TODO I don't know if this is neccessary
                return

        ch.basic_ack(delivery_tag=method.delivery_tag)
        self.numInserted += 1
        if self.numInserted % 10 == 0:
            logger.debug('  inserted {}'.format(self.numInserted))
        logger.debug("message from %d for %d" % (header['s_uniqid'], header['r_uniqid']) )

    def cassandra_insert(self, header, data):
        s_uniqid_str = nodeid_int2hexstr(header["s_uniqid"])
        
        try:
            timestamp_int = int(data[4])
        except ValueError as e:
            logger.error("QueueToRawDb: (ValueError) Error converting timestamp (%s, type: %s) into int: %s (sender: %s plugin: %s)" % (data[4], str(type(data[4])), str(e), s_uniqid_str, data[1]))
            raise
        except Exception as e:
            logger.error("QueueToRawDb: (Exception) Error converting timestamp (%s) into int: %s (sender: %s plugin: %s)" % (data[4], str(e), s_uniqid_str, data[1]))
            raise
        
        try:
            plugin_version_int = int(data[2])
        except ValueError as e:
            logger.error("QueueToRawDb: (ValueError) Error converting plugin_version (%s) into int: %s (sender: %s)" % (data[2], str(e), s_uniqid_str))
            raise
        except Exception as e:
            logger.error("QueueToRawDb: (Exception) Error converting plugin_version (%s) into int: %s (sender: %s)" % (data[2], str(e), s_uniqid_str))
            raise
        
        if not self.session:
            self.cassandra_connect()
        
        statement = "INSERT INTO sensor_data_raw (node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        if not self.prepared_statement:
            try: 
                self.prepared_statement = self.session.prepare(statement)
            except Exception as e:
                logger.error("Error preparing statement: (%s) %s" % (type(e).__name__, str(e)) )
                raise
        
        # TODO: Later we will fix this issue
        idx = [0, 1, 3, 5, 6]
        for i in idx:
            if (type(data[i]) == bytes):
                data[i] = data[i].decode('iso-8859-1')
        
        tmp = []
        for entity in data[7]:
            if (type(entity) == bytes):
                tmp.append(entity.decode('iso-8859-1'))
            else:
                tmp.append(entity)
        data[7] = tmp

        # for entity in data[7]:
        #     if (type(entity) == bytes):
        #         entity = data[i].decode('iso-8859-1')
        
        if not data[3]:
            data[3] = 'default'
        
        #                              date    plugin                      instance                sensor sensor_meta  data
        value_array = [ s_uniqid_str, data[0], data[1], plugin_version_int, data[3], timestamp_int, data[5], data[6], data[7]]
        logger.debug("inserting: %s" % (str(value_array)))
        try:
            bound_statement = self.prepared_statement.bind(value_array)
        except Exception as e:
            logger.error("QueueToRawDb: Error binding cassandra cql statement:(%s) %s -- value_array was: %s" % (type(e).__name__, str(e), str(value_array)) )
            raise

        connection_retry_delay = 1
        while True :
            # this is long term storage    
            try:
                self.session.execute(bound_statement)
            except TypeError as e:    
                 logger.error("QueueToRawDb: (TypeError) Error executing cassandra cql statement: %s -- value_array was: %s" % (str(e), str(value_array)) )
                 break
            except Exception as e:
                logger.error("QueueToRawDb: Error (type: %s) executing cassandra cql statement: %s -- value_array was: %s" % (type(e).__name__, str(e), str(value_array)) )
                if "TypeError" in str(e):
                    logger.debug("detected TypeError, will ignore this message")
                    break
                
                self.cassandra_connect()
                time.sleep(connection_retry_delay)
                if connection_retry_delay < 10:
                    connection_retry_delay = connection_retry_delay + 1
                continue
            
            break
        

    def cassandra_connect(self):
        for iTry in range(5):
            if self.cluster:
                try:
                    self.cluster.shutdown()
                except:
                    pass
                    
            self.cluster = Cluster(contact_points=[CASSANDRA_HOST])
            self.session = None
            
            iTry2 = 0
            while not self.session and iTry2 < 5:
                iTry2 += 1
                try: # Might not immediately connect. That's fine. It'll try again if/when it needs to.
                    self.session = self.cluster.connect('waggle')
                except:
                    logger.warning("QueueToRawDb: WARNING: Cassandra connection to " + CASSANDRA_HOST + " failed.")
                    logger.warning("QueueToRawDb: The process will attempt to re-connect at a later time.")
                if not self.session:
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
    p = DataProcess()
    p.start()
    
    print(__name__ + ': created process ', p)
    time.sleep(120)   
    
    while p.is_alive():
        time.sleep(10)
        
    print(__name__ + ': process is dead, time to die')
    p.join()
    
