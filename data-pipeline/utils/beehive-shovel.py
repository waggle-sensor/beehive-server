#!/usr/bin/env python3
import pika
from beehive import get_flat_export_data
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

for row in get_flat_export_data(sys.argv[1], sys.argv[2]):
    headers = {
        'node': row[0],
        'ts': row[1],
        'plugin': [row[2], row[3]],
        'sensor': [row[5], row[6]],
    }

    routing_key = '.'.join([row[2], row[3]])

    channel.basic_publish(exchange='plugins.route',
                          routing_key=routing_key,
                          properties=pika.BasicProperties(headers=headers),
                          body=row[7])
