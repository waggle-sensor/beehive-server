#!/usr/bin/env python3
import datetime
import pika
import time
import sys

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='data_0',
                             type='fanout')
    # rapid fire messages
    print('START: ', datetime.datetime.now())
    for x in range(1000):
        message = '___task #{}'.format(x)
                     
        channel.basic_publish(exchange='data_0',
                              routing_key='data_in',
                              body=message)
        print(" [x] Sent %r" % message)
        time.sleep(3)
    print('END:   ', datetime.datetime.now())
    connection.close()
