#!/usr/bin/env python3
import pika
import json
import struct


def decode_alphasense(data):
    bincounts = struct.unpack_from('<16H', data, offset=0)
    mtof = [x / 3 for x in struct.unpack_from('<4B', data, offset=32)]
    sample_flow_rate = struct.unpack_from('<f', data, offset=36)[0]
    pressure = struct.unpack_from('<I', data, offset=40)[0]
    temperature = pressure / 10.0
    sampling_period = struct.unpack_from('<f', data, offset=44)[0]
    checksum = struct.unpack_from('<H', data, offset=48)[0]
    pmvalues = struct.unpack_from('<3f', data, offset=50)

    assert pmvalues[0] <= pmvalues[1] <= pmvalues[2]
    assert sum(bincounts) & 0xFFFF == checksum

    values = {
        'bins': bincounts,
        'mtof': mtof,
        'sample flow rate': sample_flow_rate,
        'sampling period': sampling_period,
        'pm1': pmvalues[0],
        'pm2.5': pmvalues[1],
        'pm10': pmvalues[2],
    }

    if temperature > 200:
        values['pressure'] = pressure
    else:
        values['temperature'] = temperature

    return values


def callback(ch, method, properties, body):
    try:
        data = decode_alphasense(body)
        channel.basic_publish(exchange='x-plugins-out',
                              routing_key='',
                              # routing_key='alphasense.1',
                              body=json.dumps(data))
    except Exception as e:
        channel.basic_publish(exchange='x-logs',
                              routing_key='error',
                              body=repr(e))


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='x-logs', type='direct')

channel.exchange_declare(exchange='x-plugins-in', type='direct')
channel.exchange_declare(exchange='x-plugins-out', type='fanout')

channel.queue_declare(queue='alphasense.1')
channel.queue_bind(exchange='x-plugins-in',
                   queue='alphasense.1',
                   routing_key='alphasense.1')

channel.basic_consume(callback, queue='alphasense.1', no_ack=True)
channel.start_consuming()
