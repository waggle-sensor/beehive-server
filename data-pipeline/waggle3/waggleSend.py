#!/usr/bin/env python3
import argparse
from config import *
import datetime
import pika
import time
import sys

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-rate', default = 0.1)
    args = argParser.parse_args()
    print('rate = ', float(args.rate))
    period = 1.0 / float(args.rate)
    print('period = ', period)

    connection = pika.BlockingConnection(pika_params)
    channel = connection.channel()

    #channel.exchange_declare(exchange='x_data_0', type='fanout')
    # rapid fire messages
    print('START: ', datetime.datetime.now())
    for x in range(1000):
        message = '___task #{}'.format(x)

        channel.basic_publish(exchange='data-pipeline-in',
                              routing_key='',
                              body=message)
        print(" [x] Sent %r" % message)
        time.sleep(period)
    print('END:   ', datetime.datetime.now())
    connection.close()
