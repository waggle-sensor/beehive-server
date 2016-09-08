#!/usr/bin/env python3
import pika
from base64 import b64decode
from coresense import spec as sensorinfo
import coresense.format
from datetime import datetime
import json


def decode_coresense_frame(frame):
    if frame[0] != 0xAA:
        raise RuntimeError('invalid frame start {:02X}'.format(frame[0]))

    if frame[-1] != 0x55:
        raise RuntimeError('invalid frame end {:02X}'.format(frame[-1]))

    if frame[2] + 5 != len(frame):
        raise RuntimeError('inconsistent frame length')

    return decode_coresense_data(frame[3:-3])


def decode_coresense_data(data):
    for sensor_id, sensor_data in get_data_subpackets(data):
        try:
            name, fmt, fields = sensorinfo[sensor_id]
            data = dict(zip(fields, coresense.format.unpack(fmt, sensor_data)))
            yield name, data
        except KeyError:
            channel.basic_publish(exchange='x-logs',
                                  routing_key='error',
                                  body='unknown sensor {:02X}'.format(sensor_id))


def get_data_subpackets(data):
    subpackets = []

    offset = 0

    while offset < len(data):
        sensor_id = data[offset + 0]
        length = data[offset + 1] & 0x7F
        valid = data[offset + 1] & 0x80 == 0x80
        offset += 2

        sensor_data = data[offset:offset + length]
        offset += length

        if valid:
            subpackets.append((sensor_id, sensor_data))

    if offset != len(data):
        raise RuntimeError('subpacket lengths do not total to payload length')

    return subpackets


def callback(ch, method, properties, body):
    headers = properties.headers

    if headers['sensor'] == ['raw', 'data']:
        for sensor, data in decode_coresense_data(b64decode(body)):
            payload = {
                'node_id': '00A',
                'node_config': '123abc',
                'datetime': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'sensor': sensor,
                'data': data
            }

            channel.basic_publish(exchange='x-plugins-out',
                                  routing_key='',
                                  # routing_key='envsense.2',
                                  body=json.dumps(payload))


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='x-logs', type='direct')

channel.exchange_declare(exchange='x-plugins-in', type='direct')
channel.exchange_declare(exchange='x-plugins-out', type='fanout')

channel.queue_declare(queue='envsense.2')
channel.queue_bind(exchange='x-plugins-in',
                   queue='envsense.2',
                   routing_key='envsense.2')

channel.basic_consume(callback, queue='envsense.2', no_ack=True)
channel.start_consuming()
