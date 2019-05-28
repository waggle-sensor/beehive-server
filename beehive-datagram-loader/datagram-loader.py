#!/use/bin/env python3

# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

import csv
import datetime
import sys

import pika
import psycopg2
import waggle.protocol


psql_conn = psycopg2.connect("dbname='postgres' host='beehive-postgres' user='postgres' password='waggle'")
cursor = psql_conn.cursor()

rmq_conn = pika.BlockingConnection(pika.URLParameters('amqp://router:router@beehive-rabbitmq'))
channel = rmq_conn.channel()
queue = 'to-node-0000000000000000'
channel.queue_declare(queue=queue, durable=True)

csvout = csv.writer(sys.stdout)


def unpack_messages_and_sensorgrams(body):
    for message in waggle.protocol.unpack_waggle_packets(body):
        for datagram in waggle.protocol.unpack_datagrams(message['body']):
            for sensorgram in waggle.protocol.unpack_sensorgrams(datagram['body']):
                yield message, datagram, sensorgram


def message_handler(ch, method, properties, body):
    for message, datagram, sensorgram in unpack_messages_and_sensorgrams(body):
        timestamp = datetime.datetime.fromtimestamp(sensorgram['timestamp'])
        node_id = message['sender_id']
        
        plugin_id = datagram['plugin_id']
        plugin_instance = datagram['plugin_instance']

        csvout.writerow([str(timestamp), node_id, plugin_id, plugin_instance, str(body)])
        sys.stdout.flush()

        cursor.execute(
            """
            INSERT INTO datagrams (timestamp, node_id, plugin_id, plugin_instance, sensorgrams)
                VALUES (%s, %s, %s, %s, %s);
            """, 
            (timestamp, node_id, plugin_id, plugin_instance, body)
        )

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue, message_handler)
channel.start_consuming()
