#!/usr/bin/env python3
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model


class MessageData(Model):

    node_id = columns.Text(partition_key=True)
    date = columns.Date(partition_key=True)
    topic = columns.Text(primary_key=True)
    created_at = columns.DateTime(primary_key=True)
    received_at = columns.DateTime(required=True)
    body = columns.Blob(required=True)


class MessageLog(Model):

    __options__ = {
        'default_time_to_live': 259200,
    }

    node_id = columns.Text(partition_key=True)
    topic = columns.Text(primary_key=True)
    created_at = columns.DateTime(primary_key=True)
    received_at = columns.DateTime(required=True)
    body = columns.Blob(required=True)


connection.setup(['localhost'], 'waggle')

q = MessageData.objects()

for r in q:
    print('node_id:', r.node_id)
    print('created_at:', r.created_at)
    print('body:', r.body)
    print()

print('count:', q.count())
