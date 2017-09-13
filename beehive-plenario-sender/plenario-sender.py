#!/usr/bin/env python
import os
import random
import boto3
import datetime
import json
import logging
import pika
import re
from pprint import pprint


BEEHIVE_DEPLOYMENT = os.environ.get('BEEHIVE_DEPLOYMENT', '/')


global nCallbacks
nCallbacks = 0

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
    region_name='us-east-1')

# set the logging level - the default prints so many debug messages that it slows things down
logging.getLogger('botocore').setLevel(logging.WARNING)


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
0000001e0610ba89
0000001e0610b9e7
0000001e0610b9fd
''')


def map_values(sensor, values):
    for key, value in values.items():
        if key in mapping[sensor]:
            yield mapping[sensor][key], value


def callback(ch, method, properties, body):
    global nCallbacks

    node_id = properties.reply_to
    sensor = properties.type
    timestamp = datetime.fromtimestamp(properties.timestamp / 1000)

    if node_id in allowed_nodes and sensor in mapping:
        payload = {
            'network': 'array_of_things_chicago',
            'meta_id': 0,
            'node_id': node_id,
            'sensor': sensor,
            'data': dict(map_values(sensor, json.loads(body.decode()))),
            'datetime': timestamp.strftime('%Y-%m-%dT%H:%M:%S'),
        }

        kinesis_client.put_record(**{
            'StreamName': 'ObservationStream',
            'PartitionKey': str(random.random()),
            'Data': json.dumps(payload)
        })

        if nCallbacks % 100 == 0:
            # print(datetime.utcnow().isoformat(sep=' '), "[plenario-sender] Sent: {}    sensor={}, data={}".format(nCallbacks, sensor, body.decode()))
            print(timestamp, "[plenario-sender] Sent: {}    sensor={}, data={}".format(nCallbacks, sensor, body.decode()))
        nCallbacks += 1

    ch.basic_ack(delivery_tag=method.delivery_tag)


print("[plenario-sender] Start!")

print("[plenario-sender] mapping: \n")
pprint(mapping)
print()

print("[plenario-sender] allowed_nodes: \n")
pprint(allowed_nodes)
print()

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    port=5672,
    virtual_host=BEEHIVE_DEPLOYMENT,
    credentials=pika.PlainCredentials(
        username='plenario_sender',
        password='waggle',
    ),
    connection_attempts=10,
    retry_delay=3.0))

channel = connection.channel()

channel.queue_declare(queue='plenario', durable=True)
channel.queue_bind(queue='plenario', exchange='plugins-out')

channel.basic_consume(callback, queue='plenario')
channel.start_consuming()
