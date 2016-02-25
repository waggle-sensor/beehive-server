# dataprocess.py

import sys
sys.path.append("..")
sys.path.append("/usr/lib/waggle/")
from multiprocessing import Process, Manager
from config import *
import pika
from waggle_protocol.protocol.PacketHandler import *
from waggle_protocol.utilities.gPickler import *
import logging, time
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
                logger.error("Could not connect to RabbitMQ server \"%s\": %s" % (pika_params.host, e))
                time.sleep(1)
                continue
            break
            
    
        logger.info("Connected to RabbitMQ server \"%s\"" % (pika_params.host))        
        self.session = None
        self.cluster = None
        self.prepared_statement = None
        
        self.cassandra_connect()
        
        
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        # Declare this process's queue
        self.channel.queue_declare("data")
        try: 
            self.channel.basic_consume(self.callback, queue='data')
        except KeyboardInterrupt:
           logger.info("exiting.")
           sys.exit(0)
        except Exception as e:
           logger.error("error: %s" % (str(e)))
        
    def callback(self,ch,method,props,body):
        #TODO: this simply drops failed messages, might find a better solution!? Keeping them has the risk of spamming RabbitMQ
        try:
            header,data = unpack(body)
        except Exception as e:    
            logger.error("Error unpacking data: %s" % (str(e)))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            #time.sleep(1)
            #self.cassandra_connect()#TODO I don't know if this is neccessary
            return
            
        try:    
            data = un_gPickle(data)
        except Exception as e:    
            logger.error("Error un_gPickle data: %s" % (str(e)))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            #time.sleep(1)
            #self.cassandra_connect()#TODO I don't know if this is neccessary
            return
            
        try:
            #print "Data: ", data
            # Send the data off to Cassandra
            self.cassandra_insert(header,data)
        except Exception as e:    
            logger.error("Error inserting data: %s" % (str(e)))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            #time.sleep(1)
            #self.cassandra_connect()#TODO I don't know if this is neccessary
            return
    
            
            
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
        logger.debug("message from %d for %d" % (header['s_uniqid'], header['r_uniqid']) )

    def cassandra_insert(self,header,data):
        s_uniqid_str = nodeid_int2hexstr(header["s_uniqid"])
        
        try:
            timestamp_int = int(data[4])
        except ValueError as e:
            logger.error("(ValueError) Error converting timestamp (%s, type: %s) into int: %s (sender: %s plugin: %s)" % (data[4], str(type(data[4])), str(e), s_uniqid_str, data[1]))
            raise
        except Exception as e:
            logger.error("(Exception) Error converting timestamp (%s) into int: %s (sender: %s plugin: %s)" % (data[4], str(e), s_uniqid_str, data[1]))
            raise
        
        try:
            plugin_version_int = int(data[2])
        except ValueError as e:
            logger.error("(ValueError) Error converting plugin_version (%s) into int: %s (sender: %s)" % (data[2], str(e), s_uniqid_str))
            raise
        except Exception as e:
            logger.error("(Exception) Error converting plugin_version (%s) into int: %s (sender: %s)" % (data[2], str(e), s_uniqid_str))
            raise
        
        if not self.session:
            self.cassandra_connect()
        
        statement = "INSERT INTO sensor_data (node_id, date, plugin_id, plugin_version, plugin_instance, timestamp, sensor, sensor_meta, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        if not self.prepared_statement:
            try: 
                self.prepared_statement = self.session.prepare(statement)
            except Exception as e:
                logger.error("Error preparing statement: (%s) %s" % (type(e).__name__, str(e)) )
                raise
        
       
        
        
        if not data[3]:
            data[3] = 'default'
        
        #                              date    plugin                      instance                sensor sensor_meta  data
        value_array = [ s_uniqid_str, data[0], data[1], plugin_version_int, data[3], timestamp_int, data[5], data[6], data[7]]    
        try:
            bound_statement = self.prepared_statement.bind(value_array)
        except Exception as e:
            logger.error("Error binding cassandra cql statement:(%s) %s -- value_array was: %s" % (type(e).__name__, str(e), str(value_array)) )
            raise
    
        
    
        
        connection_retry_delay = 1
        while True :
            # this is long term storage    
            try:
                self.session.execute(bound_statement)
            except TypeError as e:    
                 logger.error("(TypeError) Error executing cassandra cql statement: %s -- value_array was: %s" % (str(e), str(value_array)) )
                 break
            except Exception as e:
                logger.error("Error (type: %s) executing cassandra cql statement: %s -- value_array was: %s" % (type(e).__name__, str(e), str(value_array)) )
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
        if self.cluster:
            try:
                self.cluster.shutdown()
            except:
                pass
                
        self.cluster = Cluster(contact_points=[CASSANDRA_HOST])
        self.session = None
        
        while not self.session:
            try: # Might not immediately connect. That's fine. It'll try again if/when it needs to.
                self.session = self.cluster.connect('waggle')
            except:
                logger.warning("WARNING: Cassandra connection to " + CASSANDRA_HOST + " failed.")
                logger.warning("The process will attempt to re-connect at a later time.")
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
