#!/usr/bin/env python3
from datetime import datetime, timedelta
from glob import glob
import sys
import csv


def read_csv_file(path):
    with open(path) as file:
        return csv.DictReader(file.readlines())


expected_nodes = set()

for path in sys.argv[1:]:
    for row in read_csv_file(path):
        expected_nodes.add(row['node_id'])


today = datetime.today()
yesterday = datetime.today() - timedelta(days=1)

for node in expected_nodes:
    print(node, yesterday.date())
    print(node, today.date())
