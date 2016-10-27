#!/usr/bin/env python3
import pika
import json
import struct
import os.path
import ssl
from urllib.parse import urlencode


def decode_alphasense(data):
    bincounts = struct.unpack_from('<16H', data, offset=0)
    # mtof = [x / 3 for x in struct.unpack_from('<4B', data, offset=32)]
    # sample_flow_rate = struct.unpack_from('<f', data, offset=36)[0]
    # pressure = struct.unpack_from('<I', data, offset=40)[0]
    # temperature = pressure / 10.0
    # sampling_period = struct.unpack_from('<f', data, offset=44)[0]
    checksum = struct.unpack_from('<H', data, offset=48)[0]
    pmvalues = struct.unpack_from('<3f', data, offset=50)

    assert pmvalues[0] <= pmvalues[1] <= pmvalues[2]
    assert sum(bincounts) & 0xFFFF == checksum

    values = {
        'bins': ','.join(map(str, bincounts)),
        # 'mtof': mtof,
        # 'sample flow rate': sample_flow_rate,
        # 'sampling period': sampling_period,
        'pm1': pmvalues[0],
        'pm2.5': pmvalues[1],
        'pm10': pmvalues[2],
    }

    # if temperature > 200:
    #     values['pressure'] = pressure
    # else:
    #     values['temperature'] = temperature

    return values


plugin = 'alphasense:1'

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
    if properties.type == 'histogram':
        values = decode_alphasense(body)

        props = pika.BasicProperties(
            app_id=properties.app_id,
            timestamp=properties.timestamp,
            reply_to=properties.reply_to,
            type='histogram',
            content_type='text/json',
        )

        channel.basic_publish(properties=props,
                              exchange='plugins-out',
                              routing_key=method.routing_key,
                              body=json.dumps(values))


channel.basic_consume(callback,
                      queue=plugin,
                      no_ack=True)

channel.start_consuming()
