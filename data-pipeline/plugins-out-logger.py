#!/usr/bin/env python
import pika
import boto3


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='x-plugins-out', type='fanout')

result = channel.queue_declare(exclusive=True)
queue = result.method.queue

channel.queue_bind(exchange='x-plugins-out', queue=queue)


def callback(ch, method, properties, body):
    print(body)


channel.basic_consume(callback, queue=queue, no_ack=True)
channel.start_consuming()
