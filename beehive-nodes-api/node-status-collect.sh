#!/bin/bash

set -e



STATS_DIR=/tmp/stats/
mkdir -p /tmp/stats/

while true
do

  set -x
  docker exec -i beehive-sshd netstat -nlp | grep -e '^tcp ..*127.0.0.1:[0-9][0-9][0-9][0-9][0-9]..*sshd: root' | awk '{print $4}' | sed 's/127.0.0.1://' > /tmp/stats/beehive-sshd-netstat.txt

  docker exec -i beehive-rabbitmq rabbitmqctl list_connections user > /tmp/stats/beehive-rabbitmq-list_connections_user.txt

  docker logs --since=5m beehive-loader-raw > /tmp/stats/beehive-loader-raw.txt

  docker logs --since=5m beehive-data-loader | cut -d',' -f2 > /tmp/stats/beehive-data-loader.txt
  
  sleep 300
  set +x
done

# /tmp/beehive-sshd-netstat.txt
# /tmp/beehive-rabbitmq-list_connections_user.txt
# /tmp/beehive-loader-raw.txt
# /tmp/beehive-data-loader.txt


# docker run --rm -ti --env-file ~/git/beehive-server/beehive.conf --net beehive -v /tmp/stats:/stats -v `pwd`:/code python:3-alpine /bin/ash
