from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
import pika
import os
import json
from datetime import datetime


RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', '5672'))
RABBITMQ_VIRTUAL_HOST = os.environ.get('RABBITMQ_VIRTUAL_HOST', '/')
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME', 'loader_metrics')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'waggle')

CASSANDRA_HOSTS = os.environ.get('CASSANDRA_HOSTS', 'cassandra').split()
CASSANDRA_KEYSPACE = os.environ.get('CASSANDRA_KEYSPACE', 'waggle')


class MetricData(Model):

    node_id = columns.Ascii(partition_key=True)
    date = columns.Date(partition_key=True)
    data_timestamp = columns.DateTime(primary_key=True)
    data = columns.Ascii(required=True)


connection.setup(CASSANDRA_HOSTS, CASSANDRA_KEYSPACE)
sync_table(MetricData)


def process_message(ch, method, properties, body):
    doc = json.loads(body.decode())

    node_id = doc['node_id']
    timestamp = datetime.strptime(doc['@timestamp'], '%Y/%m/%d %H:%M:%S')
    date = timestamp.date()

    MetricData.create(
        node_id=node_id,
        date=date,
        data_timestamp=timestamp,
        data=json.dumps(doc, separators=(',', ':')))

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(doc, flush=True)


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
channel.basic_consume(process_message, queue='metrics-to-cassandra')
channel.start_consuming()
