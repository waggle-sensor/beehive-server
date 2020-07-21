#!/usr/bin/env python3
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
import argparse
from cassandra.cluster import Cluster
import csv
import datetime
import pika
import sys
import waggle.protocol
import os
import logging
from prometheus_client import Counter, start_http_server
from random import seed
from random import sample


simulate_nodes = os.environ.get('SIMULATE_NODES')

if simulate_nodes == "1":
    seed(1)
    sequence = [i for i in range(1, 20)] # change it to random.randrange(start, stop)?
    dataloader_count = 0


from prometheus_client import Counter, start_http_server



logging.basicConfig(level=logging.INFO)


cassandra_host = os.environ.get('CASSANDRA_HOST')


cluster = Cluster([cassandra_host])
session = cluster.connect('waggle')



session.execute('''
CREATE TABLE IF NOT EXISTS waggle.data_messages_v2 (
  node_id text,
  date date,
  plugin_id text,
  plugin_version text,
  plugin_instance text,
  timestamp timestamp,
  data blob,
  PRIMARY KEY ((node_id, date), plugin_id, plugin_version, timestamp, data)
)
''')

insert_query = session.prepare('''
INSERT INTO waggle.data_messages_v2
(date, node_id, plugin_id, plugin_version, plugin_instance, timestamp, data)
VALUES (?, ?, ?, ?, ?, ?, ?)
''')


<<<<<<< HEAD
dataloader_message_counter = Counter("dataloader_message_counter", "This metric counts the number of messages for each node.", ["node_id"])
dataloader_error_counter = Counter("dataloader_error_counter", "This metric counts the number of errors for each node.", ["node_id"])

def counter(type, node_id):
    if type == "message":
        dataloader_message_counter.labels(node_id=node_id).inc(1)
    else:
        dataloader_error_counter.labels(node_id=node_id).inc(1)


=======
counters = { "message": {}, "error": {} }

def counter(type, node_id):
    if node_id not in counters[type]:
        metric_name = "dataloader_" + type + "_counter_" + node_id
        description = "This metric counts the number of the" + type + "s for each node."
        c = Counter(metric_name, description)
        counters[type][node_id] = c
    counters[type][node_id].inc(1)

 
>>>>>>> 9234f2b4480a247581edc2d3bf9ecc526a59483e
def stringify_value(value):
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, list):
        return ','.join(map(str, value))
    return repr(str(value))


def unpack_messages(body):
    try:
        yield from waggle.protocol.unpack_waggle_packets(body)
    except Exception:
        logging.exception('invalid message with body %s', body)


def unpack_messages_datagrams(body):
    for message in unpack_messages(body):
        try:
            for datagram in waggle.protocol.unpack_datagrams(message['body']):
                yield message, datagram
        except Exception:
            node_id = message['sender_id']
            logging.exception(
                'invalid message from node_id %s with body %s', node_id, body)


def unpack_messages_datagrams_sensorgrams(body):
    for message, datagram in unpack_messages_datagrams(body):
        try:
            for sensorgram in waggle.protocol.unpack_sensorgrams(datagram['body']):
                yield message, datagram, sensorgram
            if simulate_nodes == "1":
                global dataloader_count
                if dataloader_count == 100:
                    dataloader_count = 0
                    a = 0/0
        except Exception:
            if simulate_nodes == "1":
                node_id = message['sender_id']
                number = sample(sequence, 1)[0]
                node_id = "000000000000000" + str(number)
            counter("error", node_id)
            plugin_id = datagram['plugin_id']
            plugin_version = get_plugin_version(datagram)
            logging.exception('invalid message from node_id %s plugin %s %s with body %s',
                              node_id, plugin_id, plugin_version, body)
            counter("error", node_id) #########


csvout = csv.writer(sys.stdout)



def get_plugin_version(datagram):
    return '{plugin_major_version}.{plugin_minor_version}.{plugin_patch_version}'.format(**datagram)


def message_handler(ch, method, properties, body):
    for message, datagram, sensorgram in unpack_messages_datagrams_sensorgrams(body):
        ts = datetime.datetime.fromtimestamp(sensorgram['timestamp'])
        node_id = message['sender_id']
<<<<<<< HEAD

        if simulate_nodes == "1":
            global dataloader_count
            dataloader_count += 1
            number = sample(sequence, 1)[0]
            node_id = "000000000000000" + str(number)
            print("dataloader_count: " + str(dataloader_count))

=======
>>>>>>> 9234f2b4480a247581edc2d3bf9ecc526a59483e
        plugin_id = str(datagram['plugin_id'])
        plugin_version = str(get_plugin_version(datagram))
        plugin_instance = str(datagram['plugin_instance'])

        sub_id = message['sender_sub_id']
        sensor = str(sensorgram['id'])
        parameter = str(sensorgram['sub_id'])
        value = stringify_value(sensorgram['value'])

        csvout.writerow([
            ts,
            node_id,
            sub_id,
            plugin_id,
            plugin_version,
            sensor,
            parameter,
            value,
        ])

        sys.stdout.flush()
        counter("message", node_id)

        session.execute(
            insert_query,
            (ts.date(), node_id, plugin_id, plugin_version, plugin_instance, ts, body))

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():

    start_http_server(8000) # start up the server to expose the metrics
<<<<<<< HEAD
    
=======

>>>>>>> 9234f2b4480a247581edc2d3bf9ecc526a59483e
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='amqp://localhost')
    parser.add_argument('node_id')
    args = parser.parse_args()

    queue = 'to-node-{}'.format(args.node_id)

    connection = pika.BlockingConnection(pika.URLParameters(args.url))
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    channel.basic_consume(queue, message_handler)
    channel.start_consuming()



if __name__ == '__main__':
    main()



