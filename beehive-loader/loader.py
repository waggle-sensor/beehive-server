from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from datetime import datetime
import pika
import os


RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', '5672'))
RABBITMQ_VIRTUAL_HOST = os.environ.get('RABBITMQ_VIRTUAL_HOST', '/')
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME', 'loader_metrics')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'waggle')

CASSANDRA_HOSTS = os.environ.get('CASSANDRA_HOSTS', 'cassandra').split()
CASSANDRA_KEYSPACE = os.environ.get('CASSANDRA_KEYSPACE', 'waggle')


class MessageData(Model):

    node_id = columns.Text(partition_key=True)
    date = columns.Date(partition_key=True)
    topic = columns.Text(primary_key=True)
    created_at = columns.DateTime(primary_key=True)
    received_at = columns.DateTime(required=True)
    body = columns.Blob(required=True)


def process_message(ch, method, properties, body):
    received_at = datetime.now()
    created_at = datetime.fromtimestamp(properties.timestamp // 1000)

    MessageData.create(
        node_id=properties.reply_to[-12:],
        date=created_at.date(),
        topic=method.routing_key,
        created_at=created_at,
        received_at=received_at,
        body=body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


connection.setup(['127.0.0.1'], 'waggle')
sync_table(MessageData)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    virtual_host=RABBITMQ_VIRTUAL_HOST,
    credentials=pika.PlainCredentials(
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
    ),
    connection_attempts=10,
    retry_delay=3.0))

channel = connection.channel()
# channel.basic_qos(prefetch_count=1)
channel.basic_consume(process_message, queue='data-to-cassandra')
channel.start_consuming()
