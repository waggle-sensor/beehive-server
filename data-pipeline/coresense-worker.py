#!/usr/bin/env python3
import pika


def callback(ch, method, properties, body):
    headers = properties.headers
    print(headers)
    print(body)
    print()


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='plugins.route',
                         type='direct')

channel.queue_declare(queue='plugins.envsense.2')

channel.queue_bind(queue='plugins.envsense.2',
                   exchange='plugins.route',
                   routing_key='envsense.2')

channel.basic_consume(callback, queue='plugins.envsense.2', no_ack=True)
channel.start_consuming()

# ...can also do per-sensor-routing for more granularity...
# ...that's a pretty interesting idea...
# that way things like a binary blob can get separated out totally.
# other values can get filtered and organized into specialized
# processing bins with calibration data getting pulled into them
# queue='sensor.tmp112'
