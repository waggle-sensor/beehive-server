#!/usr/bin/env python3
import json
import pika
import os
import re

plugin = 'gps:1'

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    port=5672,
    virtual_host=os.environ.get('BEEHIVE_DEPLOYMENT', 'development'),
    credentials=pika.PlainCredentials(
        username='worker_gps',
        password='worker',
    ),
    connection_attempts=10,
    retry_delay=3.0,
))

channel = connection.channel()

channel.exchange_declare(exchange='plugins-in',
                         exchange_type='direct',
                         durable=True)

channel.exchange_bind(source='data-pipeline-in',
                      destination='plugins-in')

channel.queue_declare(queue=plugin,
                      durable=True)

channel.queue_bind(queue=plugin,
                   exchange='plugins-in',
                   routing_key=plugin)

channel.exchange_declare(exchange='plugins-out',
                         exchange_type='fanout',
                         durable=True)


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

    channel.basic_publish(properties=properties,
                          exchange='plugins-out',
                          routing_key=method.routing_key,
                          body=data)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(callback, queue=plugin, no_ack=False)
channel.start_consuming()
