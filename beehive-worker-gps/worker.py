#!/usr/bin/env python3
import json
import pika
import os
import re

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', '5672'))
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME', 'worker_gps')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'worker')
BEEHIVE_DEPLOYMENT = os.environ.get('BEEHIVE_DEPLOYMENT', '/')

pattern = re.compile("(.+)\*(.+)\'(.+)")


def callback(ch, method, properties, body):
    lat, lon, alt = body.decode().split(',')

    m = pattern.match(lat)
    lat_deg = float(m.group(1))
    lat_min = float(m.group(2))
    lat_dir = m.group(3)

    m = pattern.match(lon)
    lon_deg = float(m.group(1))
    lon_min = float(m.group(2))
    lon_dir = m.group(3)

    alt_val = float(alt[:-1])

    data = json.dumps({
        'lat_deg': lat_deg,
        'lat_min': lat_min,
        'lat_dir': lat_dir,
        'lon_deg': lon_deg,
        'lon_min': lon_min,
        'lon_dir': lon_dir,
        'alt': alt_val
    })

    properties.content_type = 'text/json'

    ch.basic_publish(properties=properties,
                     exchange='plugins-out',
                     routing_key=method.routing_key,
                     body=data)

    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    virtual_host=BEEHIVE_DEPLOYMENT,
    credentials=pika.PlainCredentials(
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
    ),
    connection_attempts=10,
    retry_delay=3.0))

channel = connection.channel()

plugin = 'gps:1'
channel.queue_declare(queue=plugin, durable=True)
channel.queue_bind(queue=plugin, exchange='plugins-in', routing_key=plugin)
channel.basic_consume(callback, queue=plugin, no_ack=False)
channel.start_consuming()
