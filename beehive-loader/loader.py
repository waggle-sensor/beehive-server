from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from datetime import datetime
import pika
import os


# Model for long term data storage.
class MessageData(Model):

    node_id = columns.Text(partition_key=True)
    date = columns.Date(partition_key=True)
    topic = columns.Text(primary_key=True)
    created_at = columns.DateTime(primary_key=True)
    received_at = columns.DateTime(required=True)
    body = columns.Blob(required=True)


# Model for 72-hour rolling message log.
class MessageLog(Model):

    __options__ = {
        'default_time_to_live': 259200,
    }

    node_id = columns.Text(partition_key=True)
    topic = columns.Text(primary_key=True)
    created_at = columns.DateTime(primary_key=True)
    received_at = columns.DateTime(required=True)
    body = columns.Blob(required=True)


def process_message(ch, method, properties, body):
    # Unpack and sanitize headers and properties.
    node_id = properties.reply_to[-12:]
    received_at = datetime.utcnow()
    created_at = datetime.fromtimestamp(properties.timestamp // 1000)
    topic = method.routing_key

    # Commit message to long term storage.
    MessageData.create(
        node_id=node_id,
        date=created_at.date(),
        topic=topic,
        created_at=created_at,
        received_at=received_at,
        body=body)

    # Commit message to short term, rolling buffer.
    MessageLog.create(
        node_id=node_id,
        topic=topic,
        created_at=created_at,
        received_at=received_at,
        body=body)

    # Only ack message after all commits are successful. Combined with
    # idempotence of commits, this provides strong consistency guarentees.
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection.setup(
    CASSANDRA_HOSTS=os.environ.get('CASSANDRA_HOSTS', 'cassandra').split(),
    CASSANDRA_KEYSPACE=os.environ.get('CASSANDRA_KEYSPACE', 'waggle'))

sync_table(MessageData)
sync_table(MessageLog)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.environ.get('RABBITMQ_HOST', 'rabbitmq'),
    port=int(os.environ.get('RABBITMQ_PORT', None)),
    virtual_host=os.environ.get('RABBITMQ_VIRTUAL_HOST', None),
    credentials=pika.PlainCredentials(
        username=os.environ.get('RABBITMQ_USERNAME', 'loader'),
        password=os.environ.get('RABBITMQ_PASSWORD', 'waggle'),
    ),
    connection_attempts=10,
    retry_delay=3.0))

channel = connection.channel()
# channel.basic_qos(prefetch_count=1)
channel.basic_consume(process_message, queue='data-to-cassandra')
channel.start_consuming()
