#!/usr/bin/env python3
from datetime import datetime, timedelta
from glob import glob
import sys
import csv


def read_csv_file(path):
    with open(path) as file:
        return csv.DictReader(file.readlines())


for path in sys.argv[1:]:
    for row in read_csv_file(path):
        node_id = row['node_id']

        start = datetime.strptime(
            row['start_timestamp'], '%Y/%m/%d %H:%M:%S').date()

        try:
            end = datetime.strptime(
                row['end_timestamp'], '%Y/%m/%d %H:%M:%S').date()
        except ValueError:
            end = datetime.today().date()

        t = start

        while t <= end:
            print(node_id, t)
            t += timedelta(days=1)
