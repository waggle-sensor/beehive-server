#!/usr/bin/env python3
import os.path
import pika
import ssl
from urllib.parse import urlencode
from datetime import datetime


url = 'amqps://node:waggle@localhost:23181?{}'.format(urlencode({
    'ssl': 't',
    'ssl_options': {
        'certfile': '/mnt/waggle/SSL/node/cert.pem',
        'keyfile': '/mnt/waggle/SSL/node/key.pem',
        'ca_certs': '/mnt/waggle/SSL/waggleca/cacert.pem',
        'cert_reqs': ssl.CERT_REQUIRED
    }
}))

connection = pika.BlockingConnection(pika.URLParameters(url))

channel = connection.channel()

channel.queue_declare(queue='monitor-logs', durable=True)
channel.queue_bind(queue='monitor-logs', exchange='logs', routing_key='#')


def getpriority(levelno):
    if levelno >= 50:
        return 2
    elif levelno >= 40:
        return 3
    elif levelno >= 30:
        return 4
    elif levelno >= 20:
        return 6
    elif levelno >= 10:
        return 7
    else:
        return 6


def callback(ch, method, properties, body):
    headers = properties.headers

    node_id = properties.reply_to[4:].lower()
    priority = getpriority(headers['value'])

    print('<{}>{} {}'.format(priority, node_id, body.decode()), flush=True)


channel.basic_consume(callback, queue='monitor-logs', no_ack=True)
channel.start_consuming()
