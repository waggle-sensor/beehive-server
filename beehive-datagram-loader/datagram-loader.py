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


# connect to postgres
psql_conn = psycopg2.connect("dbname='postgres' host='beehive-postgres' user='postgres' password='waggle'")
cursor = psql_conn.cursor()

# build the table of plugin IDs
plugins = {}
cursor.execute("SELECT packet_id, version, id, name FROM plugins")
for row in cursor.fetchall():
    plugins[(row[0], row[1])] = (row[2], row[3])

# build the table of sensors IDs
sensors = {}
cursor.execute("SELECT packet_sensor_id, packet_parameter_id, id, sensor, parameter FROM sensors")
for row in cursor.fetchall():
    sensors[(row[0], row[1])] = (row[2], row[3], row[4])

# connect to rabbit
rmq_conn = pika.BlockingConnection(pika.URLParameters('amqp://router:router@beehive-rabbitmq'))
channel = rmq_conn.channel()
queue = 'to-node-0000000000000000'
channel.queue_declare(queue=queue, durable=True)

# log out to STDOUT using CSV format
csvout = csv.writer(sys.stdout)


def unpack_messages_and_sensorgrams(body):
    for message in waggle.protocol.unpack_waggle_packets(body):
        for datagram in waggle.protocol.unpack_datagrams(message['body']):
            for sensorgram in waggle.protocol.unpack_sensorgrams(datagram['body']):
                yield message, datagram, sensorgram


def get_plugin_version(datagram):
    return '{plugin_major_version}.{plugin_minor_version}.{plugin_patch_version}'.format(**datagram)


def message_handler(ch, method, properties, body):
    for message, datagram, sensorgram in unpack_messages_and_sensorgrams(body):
        # pull the timestamp and node id from the packet info
        timestamp = datetime.datetime.fromtimestamp(sensorgram['timestamp'])
        node_id = message['sender_id']

        # pull the plugin information from the packet and lookup the DB ID
        plugin_packet_id = datagram['plugin_id']
        plugin_version = get_plugin_version(datagram)
        plugin_instance = datagram['plugin_instance']
        
        try:
            (plugin_id, plugin_name) = plugins[(str(plugin_packet_id), plugin_version)]
        except:
            sys.stderr.write(f'Could not lookup plugin for {plugin_packet_id} {puglin_version}')
            sys.stderr.flush()
            continue

        # dump to STDOUT
        csvout.writerow([str(timestamp), node_id, plugin_name, plugin_version, plugin_instance, str(body)])
        sys.stdout.flush()

        # insert the packet into the datagrams table
        try:
            cursor.execute(
                """
                INSERT INTO datagrams (timestamp, node_id, plugin_id, plugin_instance, body)
                    VALUES (%s, %s, %s, %s, %s);
                """,
                (timestamp, node_id, plugin_id, plugin_instance, body)
            )
        except Exception as e:
            sys.stderr.write(f'Could not insert datagram: {e}')
            sys.stderr.flush()
            continue
        
        # pull the sensor information from the sensorgram and lookup the DB ID
        try:
            (sensor_id, sensor, parameter) = sensors[(str(sensorgram['sensor_id']), str(sensorgram['parameter_id']))]
        except:
            sys.stderr.write(f'Could not lookup sensor for {str(sensorgram['sensor_id'])} {str(sensorgram['parameter_id'])}')
            sys.stderr.flush()
            continue
        
        # get the raw value and convert to HRF
        raw_value = sensorgram['value']
        try:
            # TODO: convert to clean, hrf value
            value = 'DUNNO YET'
        except Exception as e:
            sys.stderr.write(f'Could not covert value: {e}')
            sys.stderr.flush()
            continue

        # insert the measurement from the sensorgram into the measurements table
        try:
            cursor.execute(
                """
                INSERT INTO measurements (timestamp, node_id, sensor_id, plugin_id, raw_value, value)
                  VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (timestamp, node_id, sensor_id, plugin_id, raw_value, value)
            )

    # ack message so the node can purge it from its local RMQ
    ch.basic_ack(delivery_tag=method.delivery_tag)

# start consuming messages
channel.basic_consume(queue, message_handler)
channel.start_consuming()
