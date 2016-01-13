#!/usr/bin/env python
"""
    This module sets up and runs the waggle server.
"""
import sys, pika, logging, argparse, logging, logging.handlers
from config import *
from WaggleRouter import WaggleRouter
from utilitiesprocess import UtilProcess
from multiprocessing import Manager
from registrationprocess import RegProcess
from dataprocess import DataProcess
from cassandra.cluster import Cluster
import time

import os
import signal


#pika is a bit too verbose...
logging.getLogger('pika').setLevel(logging.ERROR)
logging.getLogger('cassandra').setLevel(logging.ERROR)


logger = logging.getLogger(__name__)


# The number of processes of each type to run on this server instance
NUM_ROUTER_PROCS = 1
NUM_DATA_PROCS = 14
NUM_REGISTRATION_PROCS = 1
NUM_UTIL_PROCS = 1

exchage_list = ["waggle_in","internal"]

# Permanant queue bindings
queue_bindings = {
    "incoming"     : ("waggle_in","in"),
    "registration" : ("internal","registration"),
    "util"         : ("internal","util"),
    "data"         : ("internal","data")
}

# from: http://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/
class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO, prefix=''):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''
        self.prefix = prefix
 
    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, self.prefix+line.rstrip())

    def flush(self):
        pass




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', dest='enable_logging', help='write to log files instead of stdout', action='store_true')
    args = parser.parse_args()
    
        
    if args.enable_logging:
        # 5 times 10MB
        sys.stdout.write('logging to '+LOG_FILENAME+'\n')
        log_dir = os.path.dirname(LOG_FILENAME)
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
        
        #stdout_logger = logging.getLogger('STDOUT')
        sl = StreamToLogger(logger, logging.INFO, 'STDOUT: ')
        sys.stdout = sl
 
        #stderr_logger = logging.getLogger('STDERR')
        sl = StreamToLogger(logger, logging.ERROR, 'STDERR: ')
        sys.stderr = sl
        
        handler.setFormatter(formatter)
        root_logger.handlers = []
        root_logger.addHandler(handler)



    # Create a manager to handle some shared memory, like the routing table.
    manager = Manager()
    #The shared routing table that all routers use
    #routing_table = manager.dict()
    node_table = manager.dict()

    # DEPRECATED
    # Add node queue bindings that are already registered
    #if os.path.isfile('registrations/nodes.txt'): 
    #    with open('registrations/nodes.txt') as file_:
    #       for line in file_:
    #            if line and line != '\n':
    #                line = line[:-1] #Cut off the newline character
    #                info = line.split(":")
    #                queue_bindings[info[1]] = ("internal",info[1])
    #                routing_table[int(info[0])] = info[1]

    cassandra_session = None
    while cassandra_session == None:     
        try:    
            cassandra_cluster = Cluster(contact_points=[CASSANDRA_HOST])
        except Exception as e:
            logger.error("Connecting to cassandra failed (%s): %s" % ( CASSANDRA_HOST ,str(e) ) )
            time.sleep(1)
            continue
            
        try: # Might not immediately connect. That's fine. It'll try again if/when it needs to.
            cassandra_session = cassandra_cluster.connect()
        except Exception as e:
            logger.error("(self.cluster.connect): Cassandra connection to " + CASSANDRA_HOST + " failed: " + str(e))
            time.sleep(3)
            continue
    
    waggle_nodes = []
    
    for statement in [ keyspace_cql , nodes_cql, "select node_id, timestamp, queue, name from waggle.nodes"]:
        try: 
            cassandra_session.execute(statement)
        except Exception as e:
            logger.error("(self.session.execute(statement)) failed. Statement: %s Error: %s " % (statement, str(e)) )
            sys.exit(1)            
    
    
    num_nodes=0   
    for node in waggle_nodes:
        num_nodes+=1
        node_table[node.node_id] = {'node_id': node.node_id,
                                    'queue' : node.queue,
                                    'name': node.name}
                    #'device_dict' : node.device_dict,
                    #'priority_order' : node.priority_order} 
        queue_bindings[node.queue] = ("internal",node.queue)
        logger.debug("loading node information for node %s" % (node.node_id) )
    
    logger.debug("number of nodes: %d" % (num_nodes)) 


    cassandra_cluster.shutdown()
    

    #Connect to rabbitMQ
    try:
        rabbitConn = pika.BlockingConnection(pika_params)
    except Exception as e:
        logger.error("Could not connect to RabbitMQ server \"%s\": %s" % (pika_params.host, str(e)))
        sys.exit(1)
    
    logger.info("Connected to RabbitMQ server \"%s\"" % (pika_params.host))
    
    rabbitChannel = rabbitConn.channel()

    #Declare all of the appropriate exchanges, queues, and bindings

    for queueName in queue_bindings.keys():
        rabbitChannel.queue_declare(queueName)

    for exchName in exchage_list:
        rabbitChannel.exchange_declare(exchName)
    for key in queue_bindings.keys():
        bind = queue_bindings[key]
        rabbitChannel.queue_bind(exchange=bind[0], queue=key, routing_key=bind[1])


    #start the processes
    router_procs = []
    for i in range (0,NUM_ROUTER_PROCS):
        new_router = WaggleRouter(node_table)
        new_router.start()
        router_procs.append(new_router)
    logger.info("%d routing processes online." % (NUM_ROUTER_PROCS))

    util_procs = []
    for i in range (0,NUM_UTIL_PROCS):
        new_util = UtilProcess()
        new_util.start()
        util_procs.append(new_util)
    logger.info("Utility processes online.")

    reg_procs = []
    for i in range (0,NUM_REGISTRATION_PROCS):
        new_reg = RegProcess(node_table)
        new_reg.start()
        reg_procs.append(new_reg)
    logger.info("Registration processes online.")

    data_procs = []
    for i in range (0,NUM_DATA_PROCS):
        new_data = DataProcess()
        new_data.start()
        data_procs.append(new_reg)
    logger.info("Data forwarding processes online.")




    logger.info("All processes online. Server is fully operational.")



    # Future work: This is where server commands should be processed.
    # This could be accomplished by reading from something like a multiprocessing queue
    # and then performing whatever needs to be done right here.
    # A separate command-line process might be a good way to do this, making sure that
    # it has sole control over standard in/out.
    try:
        while True:
            for i in range(0,len(router_procs)):
                if not router_procs[i].is_alive():
                    new_router = WaggleRouter(node_table)
                    router_procs[i] = new_router
            for i in range(0,len(data_procs)):
                if not data_procs[i].is_alive():
                    new_data = DataProcess()
                    data_procs[i] = new_data

            for i in range(0,len(reg_procs)):
                if not reg_procs[i].is_alive():
                    new_reg = RegProcess(node_table)
                    reg_procs[i] = new_reg

            for i in range(0,len(util_procs)):
                if not util_procs[i].is_alive():
                    new_util = UtilProcess()
                    util_procs[i] = new_util

            time.sleep(3)
    except KeyboardInterrupt:
       logger.info("exiting.")
       sys.exit(0)
    except Exception as e:
       logger.error("error: %s" % (str(e)))
