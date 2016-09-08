#!/usr/bin/env python3
#import multiprocessing
import functools
import pika
import sys
import time

''' 
Communication pipeline configuration.

    Notation
        P = Producer
        C = Consumer
        X = eXchange (fanout)
        Q = Queue
        
Here is the data flow diagram.  
Data flows from parent to its immediate children.
Children are represented by (new-line + indent) as in Python

P(WaggleRouter)
    Q(data_in)
        X(data_raw)
            Q(db_raw)
                C(Table1Write, writes to TABLE_1)
            Q(decode_in)
                C(Plugin2Write, plugin_2)
                    X(data_decoded)
                        Q(plenario_in)
                            C(PlenarioWrite, boto to plenario)
                        Q(db_decoded)
                            C(Table2Write, writes to TABLE_2)
            Q(logfile_in)
                C(LogfileInWrite, write raw data to logfile)
            Q(slack_in)
                C(SlackInWrite, send messages to Slack when appropriate, eg. node comes online)
'''

def CallbackPushToQueue(channel, method, properties, body, label, exchange, queueDest):
    print('_{:10s}     body = {}'.format(label, body))
    channel.basic_publish(exchange = 'data_raw',
                      routing_key = queueDest,
                      body = body)
    channel.basic_ack(delivery_tag = method.delivery_tag)
    
def CallbackPushToExchange(channel, method, properties, body, label, exchange):
    print('_{:10s}     body = {}'.format(label, body))
    channel.basic_publish(exchange = exchange,
                      routing_key = '',
                      body = body)
    channel.basic_ack(delivery_tag = method.delivery_tag)


def CallbackPrint(channel, method, properties, body, label):
    print('{:10s}     body = {}'.format(label, body))
    channel.basic_ack(delivery_tag = method.delivery_tag)
    #time.sleep(1)


def QueueInit(theChannel, exchangeName, queueName, callback):

    print('QueueInit(theChannel, exchangeName = "{}", queueName = "{}"):'.format(exchangeName, queueName))
    
    theChannel.queue_declare(queue = queueName, exclusive = True)
    
    theChannel.queue_bind(exchange = exchangeName,
                   queue = queueName)

    theChannel.basic_consume(callback,
                        queue = queueName)
                        
    theChannel.basic_qos(prefetch_count=1)
    


def Configure():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
        
    channel = connection.channel()
    
    # X(data_0)
    channel.exchange_declare(exchange='data_0',
                             type='fanout')
    # X(data_raw)
    channel.exchange_declare(exchange='data_raw',
                             type='fanout')
    # X(data_decoded)
    channel.exchange_declare(exchange='data_decoded',
                             type='fanout')
                             
    # Queues
    QueueInit(channel, 'data_0',       'data_in',     functools.partial(CallbackPushToExchange, label = 'X', exchange = 'data_raw'))
    QueueInit(channel, 'data_raw',     'db_raw',      functools.partial(CallbackPrint, label = '0'))
    QueueInit(channel, 'data_raw',     'decode_in',   functools.partial(CallbackPushToExchange, label = '1', exchange = 'data_decoded'))
    QueueInit(channel, 'data_raw',     'logfile_in',  functools.partial(CallbackPrint, label = '2'))
    QueueInit(channel, 'data_raw',     'slack_in',    functools.partial(CallbackPrint, label = '3'))
    
    QueueInit(channel, 'data_decoded', 'plenario_in', functools.partial(CallbackPrint, label = '4'))
    QueueInit(channel, 'data_decoded', 'db_decoded',  functools.partial(CallbackPrint, label = '5'))
    
    channel.start_consuming()

if __name__ == "__main__":
    Configure()
    