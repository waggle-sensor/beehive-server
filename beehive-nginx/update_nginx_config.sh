#!/bin/bash


NODES_API=$(docker ps | grep beehive-nodes-api | wc -l)

CHANGES=0

if [ !  -d locations ] ; then
    echo "locations subdirectory is missing"
    exit 1
fi


if [ ${NODES_API} -eq "1" ] ; then
    echo "found beehive-nodes-api"
    if [ ! -L  locations/api_nodes.conf ] ; then
        echo "symlink is missing, create one"
        set -x
        ( cd locations ; ln -s api_nodes api_nodes.conf )
        set +x
        CHANGES=1
    fi

    if [ ! -L  upstream/api_nodes.conf ] ; then
        echo "symlink is missing, create one"
        set -x
        (cd upstream ; ln -s api_nodes api_nodes.conf )
        set +x
        CHANGES=1
    fi

elif [ ${NODES_API} -eq "0" ] ; then
    echo "not found beehive-nodes-api"
    if [ -L locations/api_nodes.conf ] ; then
        rm -f locations/api_nodes.conf
        CHANGES=1
    fi

    if [ -L upstream/api_nodes.conf ] ; then
        rm -f upstream/api_nodes.conf
        CHANGES=1
    fi

else
    echo "error parsing docker ps"
fi

echo "CHANGES: ${CHANGES}"

if [ ${CHANGES} == 1 ] ; then
    echo "relaoding nginx config"
    ./reload.sh 
fi