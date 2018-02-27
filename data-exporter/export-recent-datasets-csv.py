#!/usr/bin/env python3
from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import pipeline
from collections import defaultdict
import os

cluster = Cluster(connect_timeout=60, control_connection_timeout=60.0)
session = cluster.connect('waggle')

rows = session.execute('SELECT DISTINCT node_id, date FROM sensor_data_raw')

now = datetime.utcnow()
today = now.strftime('%Y-%m-%d')
start = now - timedelta(minutes=30)

matches = [(row.node_id, row.date) for row in rows if row.node_id and row.date == today]

query = '''
SELECT node_id, plugin_name, plugin_version, timestamp, parameter, data FROM sensor_data_raw WHERE
    node_id = %s AND
    date = %s AND
    plugin_name = %s AND
    plugin_version = %s AND
    plugin_instance = %s AND
    timestamp >= %s
'''

plugins = [
    ('coresense', '3', '0'),
    ('coresense', '4', '0'),
]

allrows = []
allnoderows = defaultdict(list)

for partition_node_id, partition_date in matches:
    node_id = partition_node_id[-12:]

    noderows = allnoderows[node_id]

    for plugin_name, plugin_version, plugin_instance in plugins:
        rows = session.execute(query, (partition_node_id, partition_date, plugin_name, plugin_version, plugin_instance, start))

        for row in rows:
            for row in rows:
                try:
                    results = pipeline.decode(row)
                except KeyboardInterrupt:
                    break
                except Exception as exc:
                    continue

                for sensor, values in results.items():
                    if isinstance(values, dict):
                        enum = values.items()
                    elif isinstance(values, list) or isinstance(values, tuple):
                        enum = enumerate(values)
                    else:
                        continue

                    for name, value in enum:
                        columns = [
                            node_id,
                            row.timestamp.strftime('%Y/%m/%d %H:%M:%S'),
                            ':'.join([row.plugin_name, row.plugin_version]),
                            row.parameter,
                            sensor,
                            str(name),
                            str(value),
                        ]

                        allrows.append(columns)
                        noderows.append(columns)

# allrows.sort(key=lambda columns: (columns[1], columns[0]))

with open('static/recent.csv', 'w') as outfile:
    for columns in allrows:
        print(';'.join(columns), file=outfile)

for node_id, noderows in allnoderows.items():
    try:
        os.makedirs('datasets/2/{}'.format(node_id))
    except FileExistsError:
        pass

    with open('datasets/2/{}/recent.csv'.format(node_id), 'w') as outfile:
        for columns in noderows:
            print(';'.join(columns), file=outfile)
