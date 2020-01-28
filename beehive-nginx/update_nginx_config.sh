#!/bin/bash

# This scripts checks if certain backend services are running. 
# If they are, nginx configuration will be updated by creation of symlinks in include directories.

# The reason for this script is that nginx will not start if a backend host cannot be found.


if [ !  -d locations ] ; then
    echo "locations subdirectory is missing"
    exit 1
fi

if [ !  -d upstreams ] ; then
    echo "upstreams subdirectory is missing"
    exit 1
fi

CHANGES=0



# this assumes a one-to-one mapping of container name and include filename

for container in beehive-nodes-api beehive-minio ; do 

    echo "checking container ${container} ..."

    CONTAINER_COUNT=$(docker ps | grep ${container} | wc -l | tr -d '[:space:]' )
    echo "CONTAINER_COUNT: ${CONTAINER_COUNT}"
    if [ ${CONTAINER_COUNT} -eq 1 ] ; then
        echo "found ${container}"
        if [ ! -L  locations/${container}.conf ] ; then
            echo "symlink is missing, create one"
            set -x
            ( cd locations ; ln -s ${container} ${container}.conf )
            set +x
            CHANGES=1
        fi

        if [ ! -L  upstreams/${container}.conf ] ; then
            echo "symlink is missing, create one"
            set -x
            (cd upstreams ; ln -s ${container} ${container}.conf )
            set +x
            CHANGES=1
        fi

    elif [ ${CONTAINER_COUNT} -eq 0 ] ; then
        echo "did not find ${container}"
        if [ -L locations/${container}.conf ] ; then
            rm -f locations/${container}.conf
            CHANGES=1
        fi

        if [ -L upstreams/${container}.conf ] ; then
            rm -f upstreams/${container}.conf
            CHANGES=1
        fi

    else
        echo "error parsing docker ps"
    fi

done

echo "CHANGES: ${CHANGES}"

if [ ${CHANGES} == 1 ] ; then
    echo "relaoding nginx config"
    ./reload.sh 
fi