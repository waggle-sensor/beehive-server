#!/usr/bin/env python3
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


NUM_ROUTER_PROCS = 1
NUM_DATA_PROCS = 14
NUM_REGISTRATION_PROCS = 1
NUM_UTIL_PROCS = 1

exchage_list = [
    "waggle_in",
    "internal"
]

# Permanant queue bindings
queue_bindings = {
    "incoming"     : ("waggle_in","in"),
    "registration" : ("internal","registration"),
    "util"         : ("internal","util"),
    "data"         : ("internal","data")
}

if __name__ == "__main__":
    manager = Manager()
    node_table = manager.dict()

    print('<5>Connecting to Cassandra: {}'.format(CASSANDRA_HOST), flush=True)
    cassandra_cluster = Cluster(contact_points=[CASSANDRA_HOST])

    print('<7>Getting Cassandra session', flush=True)
    cassandra_session = cassandra_cluster.connect()

    print('<5>Setting up Cassandra tables', flush=True)
    for statement in [ keyspace_cql, type_plugin_sql, nodes_cql, registration_log_cql, sensor_data_cql]:
        cassandra_session.execute(statement)

    print('<5>Getting registered nodes', flush=True)

    waggle_nodes = []

    statement = "select node_id, timestamp, queue, name from waggle.nodes"
    try:
        waggle_nodes = cassandra_session.execute(statement)
    except Exception as e:
        logger.error("(self.session.execute(statement)) failed. Statement: %s Error: %s " % (statement, str(e)) )
        sys.exit(1)

    for node in waggle_nodes:
        node_table[node.node_id] = {'node_id': node.node_id,
                                    'queue' : node.queue,
                                    'name': node.name}
                    #'device_dict' : node.device_dict,
                    #'priority_order' : node.priority_order}
        queue_bindings[node.queue] = ("internal",node.queue)
        logger.debug("loading node information for node %s" % (node.node_id) )

    print('<5>Disconnecting from Cassandra', flush=True)
    cassandra_cluster.shutdown()

    print('<5>Connecting to RabbitMQ: {}'.format(pika_params.host), flush=True)
    rabbitConn = pika.BlockingConnection(pika_params)
    rabbitChannel = rabbitConn.channel()

    for queueName in list(queue_bindings.keys()):
        print('<5>Declaring queue: {}'.format(queueName), flush=True)
        rabbitChannel.queue_declare(queueName)

    for exchName in exchage_list:
        print('<5>Declaring exchange: {}'.format(exchName), flush=True)
        rabbitChannel.exchange_declare(exchName)

    for key in list(queue_bindings.keys()):
        bind = queue_bindings[key]
        print('<5>Binding queue to exchange: {} - {} -> {}'.format(key, bind[1], bind[0]), flush=True)
        rabbitChannel.queue_bind(exchange=bind[0], queue=key, routing_key=bind[1])

    router_procs = []

    print('<5>Starting router processes', flush=True)

    for i in range(NUM_ROUTER_PROCS):
        print('<7>Starting router process {}'.format(i), flush=True)
        new_router = WaggleRouter(node_table)
        new_router.start()
        router_procs.append(new_router)

    util_procs = []

    print('<5>Starting utility processes', flush=True)

    for i in range(NUM_UTIL_PROCS):
        print('<7>Starting utililty process {}'.format(i), flush=True)
        new_util = UtilProcess()
        new_util.start()
        util_procs.append(new_util)

    reg_procs = []

    print('<5>Starting registration processes', flush=True)

    for i in range(NUM_REGISTRATION_PROCS):
        print('<7>Starting registration process {}'.format(i), flush=True)
        new_reg = RegProcess(node_table)
        new_reg.start()
        reg_procs.append(new_reg)

    data_procs = []

    print('<5>Starting data processes', flush=True)

    for i in range(NUM_DATA_PROCS):
        print('<7>Starting data processes {}'.format(i), flush=True)
        new_data = DataProcess()
        new_data.start()
        data_procs.append(new_data)

    print('<5>Server ready', flush=True)

    # Future work: This is where server commands should be processed.
    # This could be accomplished by reading from something like a multiprocessing queue
    # and then performing whatever needs to be done right here.
    # A separate command-line process might be a good way to do this, making sure that
    # it has sole control over standard in/out.
    try:
        while True:
            for i in range(0,len(router_procs)):
                if not router_procs[i].is_alive():
                    router_procs[i] = WaggleRouter(node_table)
                    router_procs[i].start()

            for i in range(0,len(data_procs)):
                if not data_procs[i].is_alive():
                    data_procs[i] = DataProcess()
                    data_procs[i].start()

            for i in range(0,len(reg_procs)):
                if not reg_procs[i].is_alive():
                    reg_procs[i] = RegProcess(node_table)
                    reg_procs[i].start()

            for i in range(0,len(util_procs)):
                if not util_procs[i].is_alive():
                    util_procs[i] = UtilProcess()
                    util_procs[i].start()

            time.sleep(3)

    except KeyboardInterrupt:
       print('<5>Stopping server', flush=True)
       sys.exit(0)
