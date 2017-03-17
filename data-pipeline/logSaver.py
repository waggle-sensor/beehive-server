#!/usr/bin/env python3
import argparse
from datetime import datetime
import pika


def callback(ch, method, properties, body):
    headers = properties.headers

    node_id = properties.reply_to[4:].lower()
    priority = headers['value']

    strUtcNow = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    print('{} <{}>{} {}'.format(strUtcNow, priority, node_id, body.decode()), flush=True)
    
    
#_______________________________________________________________________
if __name__ == '__main__':

    # command-line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--verbose', '-v', action = 'count')
    argParser.add_argument('-debug', action = 'store_true')
    args = argParser.parse_args()
    verbosity = 0 if not args.verbose else args.verbose
    if verbosity: print('args =', args)

    # set up the rabbitmq connection
    credentials = pika.PlainCredentials('server', 'waggle')
    parameters = pika.ConnectionParameters('beehive-rabbitmq', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    channel.queue_declare(queue='log-saver', durable=True)
    channel.queue_bind(queue='log-saver', exchange='logs', routing_key='#')

    channel.basic_consume(callback, queue='log-saver', no_ack=True)
    channel.start_consuming()
