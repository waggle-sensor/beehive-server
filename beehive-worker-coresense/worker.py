#!/usr/bin/env python3
import json
import pika
import os
from waggle.coresense.utils import decode_frame

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', '5672'))
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME', 'worker_coresense')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'waggle')
BEEHIVE_DEPLOYMENT = os.environ.get('BEEHIVE_DEPLOYMENT', '/')


def callback(ch, method, properties, body):
    try:
       for sensor, values in decode_frame(body).items():
            props = pika.BasicProperties(
                app_id=properties.app_id,
                timestamp=properties.timestamp,
                reply_to=properties.reply_to,
                type=sensor,
                content_type='text/json',
            )

            ch.basic_publish(properties=props,
                             exchange='plugins-out',
                             routing_key=method.routing_key,
                             body=json.dumps(values))
    except:
        print('plugin "{}" worker callback: bad message, reply_to={}, properties={}, body={}'.format(plugin, properties.reply_to, properties, body))

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

plugin = 'coresense:3'
channel.queue_declare(queue=plugin, durable=True)
channel.queue_bind(queue=plugin, exchange='plugins-in', routing_key=plugin)
channel.basic_consume(callback, queue=plugin, no_ack=False)
channel.start_consuming()
