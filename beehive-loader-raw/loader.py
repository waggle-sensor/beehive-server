from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.management import create_keyspace_simple
from cassandra.cqlengine.models import Model
from datetime import datetime
import pika
import os

BEEHIVE_DEPLOYMENT = os.environ.get('BEEHIVE_DEPLOYMENT', 'development')


class SensorData(Model):

    node_id = columns.Text(partition_key=True)
    date = columns.Date(partition_key=True)
    created_at = columns.DateTime(primary_key=True)
    received_at = columns.DateTime()
    plugin_id = columns.Text(primary_key=True)
    topic = columns.Text()
    data = columns.Blob()


def process_message(ch, method, properties, body):
    user_id = properties.user_id
    received_at = datetime.utcnow()
    created_at = datetime.utcfromtimestamp(properties.timestamp // 1000)
    plugin_id = method.routing_key
    topic = properties.type

    SensorData.create(
        node_id=user_id,
        date=received_at.date(),
        created_at=created_at,
        received_at=received_at,
        plugin_id=plugin_id,
        topic=topic,
        data=body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    # setup cassandra connection and models
    connection.setup(['beehive-cassandra'], BEEHIVE_DEPLOYMENT)
    create_keyspace_simple(BEEHIVE_DEPLOYMENT, replication_factor=3)
    sync_table(SensorData)

    # connect to message broker
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='beehive-rabbitmq',
        port=5672,
        virtual_host=BEEHIVE_DEPLOYMENT,
        credentials=pika.PlainCredentials(
            username='loader_raw',
            password='waggle',
        ),
        connection_attempts=5,
        retry_delay=5.0))

    # get channel and start processing messages
    channel = connection.channel()

    channel.exchange_declare(
        exchange='data-pipeline-in',
        durable=True)

    channel.queue_declare(
        queue='raw-data',
        durable=True)

    channel.queue_bind(
        queue='raw-data',
        exchange='data-pipeline-in',
        routing_key='')

    channel.basic_consume(
        process_message,
        queue='raw-data')

    channel.start_consuming()
