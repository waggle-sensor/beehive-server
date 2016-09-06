#!/usr/bin/env python
import pika
import boto3


# setup rabbitmq client
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='plenario')


# setup kinesis client
kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id='*** SECRET ***',
    aws_secret_access_key='*** PASSWORD ***',
    region_name='us-east-1',
)


def callback(ch, method, properties, body):
    print(body.decode())

    kinesis_client.put_record(**{
        'StreamName': 'ObservationStream',
        'PartitionKey': 'arbitrary',
        'Data': body.decode()
    })


channel.basic_consume(callback, queue='plenario', no_ack=True)
channel.start_consuming()
