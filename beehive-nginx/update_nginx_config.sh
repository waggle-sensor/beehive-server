#!/bin/bash



if [ !  -d locations ] ; then
    echo "locations subdirectory is missing"
    exit 1
fi


if [ ! -e api_nodes_access.whitelist ]  ; then
    cp api_nodes_access.whitelist.example api_nodes_access.whitelist
fi


CHANGES=0



# this assumes a one-to-one mapping of container name and include filename

for container in beehive-nodes-api beehive-minio ; do 

    echo "checking container ${container} ..."

    NODES_API=$(docker ps | grep ${container} | wc -l)

    if [ ${NODES_API} -eq "1" ] ; then
        echo "found ${container}"
        if [ ! -L  locations/${container}.conf ] ; then
            echo "symlink is missing, create one"
            set -x
            ( cd locations ; ln -s ${container} ${container}.conf )
            set +x
            CHANGES=1
        fi

        if [ ! -L  upstream/${container}.conf ] ; then
            echo "symlink is missing, create one"
            set -x
            (cd upstream ; ln -s ${container} ${container}.conf )
            set +x
            CHANGES=1
        fi

    elif [ ${NODES_API} -eq "0" ] ; then
        echo "did not find ${container}"
        if [ -L locations/${container}.conf ] ; then
            rm -f locations/${container}.conf
            CHANGES=1
        fi

        if [ -L upstream/${container}.conf ] ; then
            rm -f upstream/${container}.conf
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