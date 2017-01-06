#!/bin/bash

if true; then
    IP='0.0.0.0'
    NODE='ffffffffffff0001'
else
    IP=http://beehive1.mcs.anl.gov
    NODE='0000001e06108202'
fi

# function to test if a string is contained in another.  Format:
#      contains aList anItem
function contains() {
    if [[ $1 =~ (^|[[:space:]])$2($|[[:space:]]) ]]; then
        echo 1
    else
        echo 0
    fi
}

bJustPrintUrls="0"
if [[ $(contains "${*}" "-q") -eq 1 ]] ; then
    bJustPrintUrls="1"
fi

function url() {
    if [ $bJustPrintUrls -eq "1" ]; then
        echo $*
    else
        echo " "
        echo "#############" $*
        echo " "
        curl "${*}"
        echo " "
    fi
}

if true; then
    url ${IP}/admin/

    url ${IP}/api/
    url ${IP}/api/1/
    url ${IP}/api/1/epoch
    url ${IP}/api/1/nodes/
    url ${IP}/api/1/nodes/?all=true
    url ${IP}/api/nodes
    
    url "${IP}/api/1/nodes/${NODE}/dates"
    url "${IP}/api/1/nodes/${NODE}/dates?version=1"
    url "${IP}/api/1/nodes/${NODE}/dates?version=2raw"
    url "${IP}/api/1/nodes/${NODE}/dates?version=2"
    url "${IP}/api/1/nodes/${NODE}/dates?version=2.1"
    
    url ${IP}/api/1/nodes_last_update/
    
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=1"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=2raw"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=2"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=2.1"

    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&limit=10"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=1&limit=10"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=2raw&limit=10"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=2&limit=10"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=2.1&limit=10"

    url "${IP}/api/1/nodes/all_dates"
    url "${IP}/api/1/nodes/all_dates?version=1"
    url "${IP}/api/1/nodes/all_dates?version=2raw"
    url "${IP}/api/1/nodes/all_dates?version=2"
    url "${IP}/api/1/nodes/all_dates?version=2&sort=asc"
    url "${IP}/api/1/nodes/all_dates?version=2&sort=desc"
    url "${IP}/api/1/nodes/all_dates?version=2.1"

    url ${IP}/
    url ${IP}/wcc/test/
    url "${IP}/wcc/test/?dog=cat&tiger=lion"
fi
echo " "
