#!/bin/bash

if [ -z ${MYSQL_HOST} ] ; then
	echo "Variable MYSQL_HOST not set"
	exit 1
fi


until [ $(docker inspect -f {{.State.Running}} beehive-mysql)_ == "true_" ]; do
    echo "waiting for ${MYSQL_HOST}..."
    sleep 1
done