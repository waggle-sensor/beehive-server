#!/usr/bin/env python3
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
import pika
import time
from datetime import datetime
import json
import random
import ssl


parameters = pika.ConnectionParameters(
    host='34.215.1.152',
    port=23181,
    credentials=pika.PlainCredentials(
        username='publisher',
        password='waggle',
    ),
    ssl=True,
    ssl_options={
        'ca_certs': '/Users/Sean/deploy-intel/easy-rsa/easyrsa3/pki/ca.crt',
        'certfile': '/Users/Sean/deploy-intel/easy-rsa/easyrsa3/pki/issued/publisher.crt',
        'keyfile': '/Users/Sean/deploy-intel/easy-rsa/easyrsa3/pki/private/publisher.key',
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
