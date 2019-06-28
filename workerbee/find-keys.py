import re
import sys
import cassandra.cluster
from datetime import date, timedelta
from itertools import product

text = sys.stdin.read()

nodes = set()

for node_key in re.findall(r'(\S+) \| ', text):
    node_id = node_key[-12:].lower()
    nodes.add(node_id)
    nodes.add(node_id.upper())
    nodes.add(node_id.rjust(16, '0'))
    nodes.add(node_id.rjust(16, '0').upper())

start_date = date(2016, 1, 1)
end_date = date.today()

dates = []

dt = start_date

while dt <= end_date:
    dates.append(dt)
    dt += timedelta(days=1)

cluster = cassandra.cluster.Cluster()
session = cluster.connect()

q = 'SELECT data FROM waggle.sensor_data_raw WHERE node_id=%s AND date=%s LIMIT 1'

for node, date in product(nodes, dates):
    r = session.execute(q, [node, date])
    if len(list(r)) > 0:
        print(node, date, flush=True)
