#!/usr/bin/env python3
import pika
import sys


def callback(ch, method, properties, body):
    print(body)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='direct-logs',
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue = result.method.queue

for level in sys.argv[1:]:
    print(level)
    print(queue)
    channel.queue_bind(queue=queue,
                       exchange='direct-logs',
                       routing_key=level)

channel.basic_consume(callback, queue=queue, no_ack=True)
channel.start_consuming()
