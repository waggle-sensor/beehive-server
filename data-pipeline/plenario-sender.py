#!/usr/bin/env python

import base64
import boto3
import json
import os
import pika
import re
import ssl

from datetime import datetime
from pprint import pprint
from urllib.parse import urlencode


# Make sure these environment variables are in your bashrc!
# Your keys must have NO SPECIAL CHARACTERS like '\' or '$' because amazon.
#
# $ vim ~/.bashrc
#
# export AWS_ACCESS_KEY="***ACCESS_KEY***"
# export AWS_SECRET_KEY="***SECRET_KEY***"
#
# Then either refresh your terminal or run source.
#
# $ source ~/.bashrc

AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-east-1',
)


def parse_node_list(table):

    return set(map(str.strip, table.strip().splitlines()))


def parse_mapping(table):
    mapping = {}

    for block in re.split('\n{2,}', table.strip()):
        sensor, *values = map(str.strip, block.splitlines())

        if sensor not in mapping:
            mapping[sensor] = {}

        for value in values:
            names = list(map(str.strip, value.split('>')))
            if len(names) == 1:
                mapping[sensor][names[0]] = names[0]
            elif len(names) == 2:
                mapping[sensor][names[0]] = names[1]

    return mapping


mapping = parse_mapping('''
TMP112
temperature

HTU21D
temperature
humidity

HIH4030
humidity

BMP180
temperature
pressure

PR103J2
temperature

TSL250RD
intensity

MMA8452Q
acceleration.x > x
acceleration.y > y
acceleration.z > z

SPV1840LR5H-B
intensity > sample

TSYS01
temperature

HMC5883L
magnetic_field.x > x
magnetic_field.y > y
magnetic_field.z > z

HIH6130
temperature
humidity

APDS-9006-020
intensity

TSL260RD
intensity

TSL250RD
intensity

MLX75305
intensity

ML8511
intensity

MLX90614
temperature

TMP421
temperature

SPV1840LR5H-B
intensity

Chemsense
reducing_gases
ethanol
no2
o3
h2s
oxidizing_gases
co
so2

SHT25
temperature
humidity

LPS25H
temperature
pressure

Si1145
intensity
intensity
intensity

BMI160
acceleration.x > accel_x
acceleration.y > accel_y
acceleration.z > accel_z
orientation.x > orient_x
orientation.y > orient_y
orientation.z > orient_z
''')

# do same kind of mapping as above node_id > external_id

allowed_nodes = parse_node_list('''
0000001e0610ba72
''')

# url = 'amqps://node:waggle@beehive1.mcs.anl.gov:23181?{}'.format(urlencode({
url = 'amqps://jbracho:password@0.0.0.0:23181?{}'.format(urlencode({
    'ssl': 't',
    'ssl_options': {
        'certfile': os.path.abspath('/mnt/waggle/SSL/beehive-server/cert.pem'),
        'keyfile': os.path.abspath('/mnt/waggle/SSL/beehive-server/key.pem'),
        'ca_certs': os.path.abspath('/mnt/waggle/SSL/waggleca/cacert.pem'),
        'cert_reqs': ssl.CERT_REQUIRED
    }
}))


def map_values(sensor, values):
    for key, value in values.items():
        if key in mapping[sensor]:
            yield mapping[sensor][key], value


def callback(ch, method, properties, body):

    node_id = properties.reply_to
    sensor = properties.type
    timestamp = datetime.fromtimestamp(properties.timestamp / 1000)

    if node_id in allowed_nodes and sensor in mapping:
        payload = {
            'meta_id': 'irrelevant',
            'node_id': node_id,
            'sensor': sensor,
            'data': dict(map_values(sensor, json.loads(body.decode()))),
            'datetime': timestamp.strftime('%Y-%m-%dT%H:%M:%S'),
        }

        kinesis_client.put_record(**{
            'StreamName': 'ObservationStream',
            'PartitionKey': 'arbitrary',
            'Data': json.dumps(payload)
        })

        print("[plenario-sender] Successfully sent: \n")
        pprint(payload)
        print()


if __name__ == "__main__":

    print("[plenario-sender] Start!")

    print("[plenario-sender] mapping: \n")
    pprint(mapping)
    print()

    print("[plenario-sender] allowed_nodes: \n")
    pprint(allowed_nodes)
    print()

    connection = pika.BlockingConnection(pika.URLParameters(url))

    channel = connection.channel()
    channel.exchange_declare(exchange='plugins-out', exchange_type='fanout', durable=True)
    channel.queue_declare(queue='plenario', durable=True)
    channel.queue_bind(queue='plenario', exchange='plugins-out')
    channel.basic_consume(callback, queue='plenario', no_ack=True)
    channel.start_consuming()
