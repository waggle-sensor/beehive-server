#!/usr/bin/env python3
import pika
import json
import os.path
import ssl
from urllib.parse import urlencode


plugin = 'gps:1'

url = 'amqps://node:waggle@beehive1.mcs.anl.gov:23181?{}'.format(urlencode({
    'ssl': 't',
    'ssl_options': {
        'certfile': os.path.abspath('SSL/node/cert.pem'),
        'keyfile': os.path.abspath('SSL/node/key.pem'),
        'ca_certs': os.path.abspath('SSL/waggleca/cacert.pem'),
        'cert_reqs': ssl.CERT_REQUIRED
    }
}))

connection = pika.BlockingConnection(pika.URLParameters(url))

channel = connection.channel()

channel.exchange_declare(exchange='plugins-in',
                         exchange_type='direct')

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
        channel.basic_publish(properties=properties,
                              exchange='plugins-out',
                              routing_key=method.routing_key,
                              body=body)


channel.basic_consume(callback,
                      queue=plugin,
                      no_ack=True)

channel.start_consuming()
