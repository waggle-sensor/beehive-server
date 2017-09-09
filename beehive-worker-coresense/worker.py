#!/usr/bin/env python3
import json
import pika
import os
from waggle.coresense.utils import decode_frame

plugin = 'coresense:3'

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.environ.get('BEEHIVE_HOST', 'beehive-rabbitmq'),
    port=os.environ.get('BEEHIVE_PORT', 5672),
    virtual_host=os.environ.get('BEEHIVE_DEPLOYMENT', 'development'),
    credentials=pika.PlainCredentials(
        username=os.environ.get('BEEHIVE_USERNAME', 'worker_coresense'),
        password=os.environ.get('BEEHIVE_PASSWORD', 'worker'),
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

            channel.basic_publish(properties=props,
                                  exchange='plugins-out',
                                  routing_key=method.routing_key,
                                  body=json.dumps(values))
    except:
        print('plugin "{}" worker callback: bad message, reply_to={}, properties={}, body={}'.format(plugin, properties.reply_to, properties, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(callback, queue=plugin, no_ack=False)
channel.start_consuming()
