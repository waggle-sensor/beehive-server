#!/usr/bin/env python3
import argparse
from config import *
import functools
import pika
import sys
import time

'''
    declare a queue with a callback that prints the data
'''

#________________________________________________________________________
def CallbackPrint(channel, method, properties, body, label):
    print('  CallbackPrint:  {}  body = {}'.format(label, body))
    channel.basic_ack(delivery_tag = method.delivery_tag)


#________________________________________________________________________
if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument('exchangeSrc')
    argParser.add_argument('queue')
    args = argParser.parse_args()

    connection = pika.BlockingConnection(pika_params)
    channel = connection.channel()

    print("{}:  exchangeSrc = '{}', queue = '{}':".format(sys.argv[0], args.exchangeSrc, args.queue))

    channel.queue_declare(queue = args.queue)

    channel.queue_bind(exchange = args.exchangeSrc,
                   queue = args.queue)

    channel.basic_consume(functools.partial(CallbackPrint, label = args.queue),
                        queue = args.queue)

    channel.basic_qos(prefetch_count=1)
    channel.start_consuming()
