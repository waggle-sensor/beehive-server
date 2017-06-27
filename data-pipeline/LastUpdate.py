#!/usr/bin/env python3

# LastUpdate.py
import os
import sys
sys.path.append(os.path.abspath('../'))
sys.path.append("/usr/lib/waggle/")
sys.path.append("/usr/lib/waggle/beehive-server")

import argparse
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
from cassandra.cqlengine.columns import Ascii
from cassandra.cqlengine.usertype import UserType
from config import *
import datetime
import logging 
from multiprocessing import Process, Manager, Queue
import pika
import time
from waggle_protocol.protocol.PacketHandler import *
from waggle_protocol.utilities.gPickler import *
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class LastUpdateProcess(Process):
    """
        This process writes the most recent date of each node's incoming raw sample
    """

    def __init__(self, q, mode, verbosity = 0):
        """
            Starts up the Data handling Process
        """
        super(LastUpdateProcess, self).__init__()
        
        self.q = q
        if mode == 'logs':
            self.input_exchange = 'logs'
            self.queue          = 'last-log'
            self.statement = "INSERT INTO nodes_last_log  (node_id, last_update) VALUES (?, ?)"
        else:
            self.input_exchange = 'data-pipeline-in'
            self.queue          = 'last-data'
            self.statement = "INSERT INTO nodes_last_data (node_id, last_update) VALUES (?, ?)"
        
        logger.info("Initializing LastUpdateProcess")
        
        # Set up the Rabbit connection
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        #Connect to rabbitMQ
        while True:
            try:
                self.connection = pika.BlockingConnection(pika_params)
            except Exception as e:
                logger.error("QueueToDb: Could not connect to RabbitMQ server \"%s\": %s" % (pika_params.host, e))
                time.sleep(1)
                continue
            break
            
        logger.info("Connected to RabbitMQ server \"%s\"" % (pika_params.host))
        self.verbosity = verbosity
        self.numInserted = 0
        self.session = None
        self.cluster = None
        self.prepared_statement = None
        
        self.cassandra_connect()
        
        
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        # Declare this process's queue
        self.channel.queue_declare(self.queue)
        
        self.channel.queue_bind(exchange = self.input_exchange,
            queue = self.queue)
        
        
        try: 
            self.channel.basic_consume(self.callback, queue=self.queue)
        except KeyboardInterrupt:
           logger.info("exiting.")
           sys.exit(0)
        except Exception as e:
           logger.error("error: %s" % (str(e)))

    def callback(self, ch, method, props, body):
        #TODO: this simply drops failed messages, might find a better solution!? Keeping them has the risk of spamming RabbitMQ
        if self.verbosity > 1:
            print('######################################')
            print('method = ', method)
            print('props = ', props)
            print('body = ', body)
        '''EXAMPLE: 
            props =  <BasicProperties(['app_id=coresense:3', 'content_type=b', 'delivery_mode=2', 'reply_to=0000001e06107d97', 'timestamp=1476135836151', 'type=frame'])>
        '''
        try:
            node_id     = props.reply_to
            self.q.put(node_id, block = False)
            if verbosity > 1: print('  caching:  ', node_id,  'self.q.qsize() = ', self.q.qsize())
        except Exception as e:
            logger.error("Error inserting (queue size = %d)  data = %s" % (self.q.qsize(), str(e)))
            logger.error(' method = {}'.format(repr(method)))
            logger.error(' props  = {}'.format(repr(props)))
            logger.error(' body   = {}'.format(repr(body)))
            ch.basic_ack(delivery_tag = method.delivery_tag)
            return

        ch.basic_ack(delivery_tag = method.delivery_tag)

    def cassandra_insert(self, values):
    
        if not self.session:
            self.cassandra_connect()
            
        if not self.prepared_statement:
            try: 
                self.prepared_statement = self.session.prepare(self.statement)
            except Exception as e:
                logger.error("Error preparing statement: (%s) %s" % (type(e).__name__, str(e)) )
                raise
        
        logger.debug("inserting: %s" % (str(values)))
        try:
            bound_statement = self.prepared_statement.bind(values)
        except Exception as e:
            logger.error("QueueToDb: Error binding cassandra cql statement:(%s) %s -- values was: %s" % (type(e).__name__, str(e), str(values)) )
            raise

        connection_retry_delay = 1
        while True :
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
        if verbosity > 1:
            logger.debug('cassandra_insert() exiting...')

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
        super(LastUpdateProcess,self).terminate()
        self.connection.close(0)
        if self.cluster:
            self.cluster.shutdown()
            
   
if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('dataToTrack', choices = ['data', 'logs'], help = 'which stream of data to track')
    argParser.add_argument('--verbose', '-v', action='count')
    args = argParser.parse_args()
    verbosity = 0 if not args.verbose else args.verbose
    
    setUpdated = set()
    q = Queue(1000)
    p = LastUpdateProcess(q, args.dataToTrack, verbosity)
    p.start()
    
    print(__name__ + ': created process ', p)
    time.sleep(10)
    
    while p.is_alive():
        # stage 1 - empty queue to setUpdated
        for _i in range(30):
            while not q.empty():
                setUpdated.add(q.get())
            if verbosity: print('len(setUpdated) = ', len(setUpdated))
            time.sleep(1)
        
        # stage 2 - periodically write setUpdated to db
        timestamp = int(datetime.datetime.utcnow().timestamp() * 1000)
        if verbosity: print('timestamp = ', timestamp, 'q.qsize() = ', q.qsize())
        for node_id in setUpdated:
            values = (node_id, timestamp)
            p.cassandra_insert(values)
            if verbosity > 1: print('  writing:  ', node_id)
        setUpdated.clear()
        
    print(__name__ + ': process is dead, time to die')
    p.join()    
