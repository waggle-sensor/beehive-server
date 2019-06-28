#!/bin/bash

source waggle-python/bin/activate
docker exec -ti beehive-cassandra cqlsh -e 'SELECT DISTINCT node_id, date FROM waggle.sensor_data_raw;' > keys.txt
python3 find-keys.py < keys.txt > found.txt
