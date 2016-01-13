# dataprocess.py

import sys
sys.path.append("..")
sys.path.append("/usr/lib/waggle/")
from multiprocessing import Process, Manager
from config import *
import pika
from waggle_protocol.protocol.PacketHandler import *
from waggle_protocol.utilities.gPickler import *
import logging
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)
from cassandra.cluster import Cluster
import time

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
                logger.error("Could not connect to RabbitMQ server \"%s\": %s" % (pika_params.host, e))
                time.sleep(1)
                continue
            break
            
    
        logger.info("Connected to RabbitMQ server \"%s\"" % (pika_params.host))        
        
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        # Declare this process's queue
        self.channel.queue_declare("data")
        self.channel.basic_consume(self.callback, queue='data')
        self.session = None
        self.cluster = None

    def callback(self,ch,method,props,body):
        #TODO: this simply drops failed messages, might find a better solution!? Keeping them has the risk of spamming RabbitMQ
        try:
            header,data = unpack(body)
        except Exception as e:    
            logger.error("Error unpacking data: %s" % (str(e)))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            time.sleep(1)
            self.cassandra_connect()#TODO I don't know if this is neccessary
            return
            
        try:    
            data = un_gPickle(data)
        except Exception as e:    
            logger.error("Error un_gPickle data: %s" % (str(e)))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            time.sleep(1)
            self.cassandra_connect()#TODO I don't know if this is neccessary
            return
            
        try:
            #print "Data: ", data
            # Send the data off to Cassandra
            self.cassandra_insert(header,data)
        except Exception as e:    
            logger.error("Error inserting data: %s" % (str(e)))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            time.sleep(1)
            self.cassandra_connect()#TODO I don't know if this is neccessary
            return
    
            
            
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
        logger.debug("message from %d for %d" % (header['s_uniqid'], header['r_uniqid']) )

    def cassandra_insert(self,header,data):
        s_uniqid_str = nodeid_int2hexstr(header["s_uniqid"])
        


        try:
            timestamp_int = int(data[4])
        except ValueError as e:
            logger.error("Error converting timestamp (%s) into int: %s" % (data[4], str(e)))
            raise

        
        value_array = [s_uniqid_str]+data[1:3]+[timestamp_int]+data[5:6]
        
        # example cassandra query:
        # OLD: INSERT INTO sensor_data (node_id, sensor_name, timestamp, data_types, data, units, extra_info) VALUES ( 0 , 'b', 1231546493284, ['d'], [0], ['f'], ['g']);
        # INSERT INTO sensor_data (node_id, date, plugin_id, plugin_version, timestamp, sensor_id, data, meta) VALUES ( 'abc_id' , '2000-01-01', 'my_plugin', 1, '2013-04-03 07:02:00',   ['mysensor1'], ['mydata'], ['metafoo']);
        try:
            # TODO: Should statement preparation not be done only once !?
            prepared_statement = self.session.prepare("INSERT INTO sensor_data" + \
                " (node_id, date, plugin_id, plugin_version, timestamp, sensor_id, data, meta)" + \
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
            bound_statement = prepared_statement.bind(value_array)
            self.session.execute(bound_statement)
        except Exception as e:
            logger.error("Error executing cassandra cql statement: %s -- value_array was: %s" % (str(e), str(value_array)) )
            raise

    def cassandra_connect(self):
        try:
            self.cluster.shutdown()
        except:
            pass
        self.cluster = Cluster(contact_points=[CASSANDRA_HOST])

        try: # Might not immediately connect. That's fine. It'll try again if/when it needs to.
            self.session = self.cluster.connect('waggle')
        except:
            logger.warning("WARNING: Cassandra connection to " + CASSANDRA_HOST + " failed.")
            logger.warning("The process will attempt to re-connect at a later time.")

    def run(self):
        self.cassandra_connect()
        self.channel.start_consuming()

    def join(self):
        super(DataProcess,self).terminate()
        self.connection.close(0)
        self.cluster.shutdown()
