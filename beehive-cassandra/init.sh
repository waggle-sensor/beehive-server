#!/bin/bash



echo "Trying to initialize cassandra, this can take a few seconds..."

n=0
until [ $n -ge 10 ]
do
   docker exec -i beehive-cassandra 'cqlsh' < init.cql && break 
   sleep 3
done


while true ; do
    docker exec -i beehive-cassandra 'cqlsh' < init.cql
    if [ $? -eq 0 ] ; then
        echo "Successfully initialized cassandra"
        break
    fi
    echo "retry in three seconds"
    sleep 3
done



