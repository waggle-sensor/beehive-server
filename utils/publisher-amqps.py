#!/usr/bin/env python3
import pika
import time
from datetime import datetime
import json
import random
import ssl


parameters = pika.ConnectionParameters(
    host='localhost',
    port=23181,
    credentials=pika.PlainCredentials(
        username='publisher',
        password='waggle',
    ),
    ssl=True,
    ssl_options={
        'ca_certs': '/path/to/ca.crt',
        'certfile': '/path/to/publisher.crt',
        'keyfile': '/path/to/publisher.key',
        'cert_reqs': ssl.CERT_REQUIRED,
    },
    connection_attempts=5,
    retry_delay=3.0,
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

print('connected', flush=True)

while True:
    now = datetime.now()
    timestr = now.strftime('%Y/%m/%d %H:%M:%S')

    utctimestamp = int(1000 * datetime.now().timestamp())

    doc = {
        '@timestamp': utctimestamp,
        'random': round(random.random(), 2),
    }

    channel.basic_publish(
        properties=pika.BasicProperties(
            app_id='metric:1',
            timestamp=utctimestamp,
            reply_to='node1',
            type='metric',
        ),
        exchange='data-pipeline-in',
        routing_key='metric:1',
        body=json.dumps(doc, separators=(',', ':')))

    print('published', flush=True)
    time.sleep(1)
