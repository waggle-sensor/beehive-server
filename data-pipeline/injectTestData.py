#!/usr/bin/env python3

# 
import argparse
import binascii
from config import *
import datetime
import logging 
import pika
import sys
import time
    
if __name__ == '__main__':
    # parse the command line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument('exchange', choices = ['data-pipeline-in', 'plugins-out'], 
        help = 'the name of the exchange into which the data is injected')
    argParser.add_argument('--period', default = 3, type = float,
        help = 'number of seconds between messages')
    argParser.add_argument('--num_messages', default = 10, type = int,
        help = 'number of messages to send')
    args = argParser.parse_args()
    print('args = ', args)
    
    # set up rabbitmq
    connection = pika.BlockingConnection(pika_params)
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)


    # loop through messages
    nMessages = 0
    while args.num_messages == 0 or nMessages < args.num_messages:
        if args.exchange == 'data-pipeline-in':
            headers = {
                'reply_to': '0000000000000000',
                'timestamp': str(int(datetime.datetime.utcnow().timestamp() * 1000)),
                'app_id': 'testsensor:v1:0',
                'type': 'param'
            }
            data = '["test":"{}"]'.format(nMessages)
        else:    #args.exchange == 'plugins-out':
            headers = {
                'reply_to': '0000000000000000',
                'timestamp': str(int(datetime.datetime.utcnow().timestamp() * 1000)),
                'meta_id' : '0',
                'data_set' : 'testsensor:v1:0',
                'type' :  'sensor0',
                'parameter' : 'param0',
                'unit' : 'unit0'
            }
            data = '["test":"{}"]'.format(nMessages)
                
        channel.basic_publish(exchange = args.exchange, 
                                properties = pika.BasicProperties(headers = 'app_id=dog'), #headers = headers), 
                                routing_key = '', 
                                body = data)
        nMessages += 1
        time.sleep(args.period)

    print('DONE injecting test data...')
    