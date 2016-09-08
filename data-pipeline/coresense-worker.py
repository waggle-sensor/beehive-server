#!/usr/bin/env python3
# import pika
from base64 import b64decode
from coresense import spec as sensorinfo
import coresense.format


def decode_coresense_frame(frame):
    if frame[0] != 0xAA:
        raise RuntimeError('invalid frame start {:02X}'.format(frame[0]))

    if frame[-1] != 0x55:
        raise RuntimeError('invalid frame end {:02X}'.format(frame[-1]))

    if frame[2] + 5 != len(frame):
        raise RuntimeError('inconsistent frame length')

    return decode_coresense_data(frame[3:-3])


def decode_coresense_data(data):
    results = []

    offset = 0

    while offset < len(data):
        sensor_id = data[offset + 0]
        length = data[offset + 1] & 0x7F
        valid = data[offset + 1] & 0x80 == 0x80
        offset += 2

        sensor_data = data[offset:offset + length]
        offset += length

        if valid:
            results.append((sensor_id, sensor_data))

    if offset != len(data):
        raise RuntimeError('subpacket lengths do not total to payload length')

    return results


data = b64decode(b'AIYAABgUzLIBgho4AoQZYyYXBIUbAAGFFAWCA1cGggHXB4gAAAEAAAAAAAmCGmAKhoCmAoYB1guEHQ8hOgyCBIkNggsVDoI1vQ+CIngQgiWHE4IZSyCGAASj4wM8HYQKphUFHoUKxgGHdB+GAhMeYm00FYMAADAagwCmsRyDAA74GYMAlKwYg4AJixeDAAFuG4MAQIQhggpMIoIKfSOCCsAkggr+JYILCSaJgD6Dh4AeAAAAJ4kACAAEAAYAAAA=')

for sensor_id, sensor_data in decode_coresense_data(data):
    try:
        name, fmt, fields = sensorinfo[sensor_id]

        print('{}'.format(name))

        for k, v in zip(fields, coresense.format.unpack(fmt, sensor_data)):
            print('  {} {}'.format(k, v))

        print()
    except KeyError:
        print('unknown sensor {:02X}'.format(sensor_id))


# def callback(ch, method, properties, body):
#     headers = properties.headers
#     print(headers)
#     print(body)
#     print()
#
#
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#
# channel = connection.channel()
#
# channel.exchange_declare(exchange='plugins.route',
#                          type='direct')
#
# channel.queue_declare(queue='plugins.envsense.2')
#
# channel.queue_bind(queue='plugins.envsense.2',
#                    exchange='plugins.route',
#                    routing_key='envsense.2')
#
# channel.basic_consume(callback, queue='plugins.envsense.2', no_ack=True)
# channel.start_consuming()
