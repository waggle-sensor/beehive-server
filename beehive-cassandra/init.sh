#!/bin/bash



echo "Trying to initialize cassandra, this can take a few seconds..."


while true ; do
    docker exec -i beehive-cassandra 'cqlsh' < init.cql
    if [ $? -eq 0 ] ; then
        echo "Successfully initialized cassandra"
        break
    fi
    echo "retry in three seconds"
    sleep 3
done



