#!/bin/sh

docker exec -ti beehive_cassandra.1.$(docker service ps -q --no-trunc -f 'name=beehive_cassandra.1' beehive_cassandra) cqlsh
