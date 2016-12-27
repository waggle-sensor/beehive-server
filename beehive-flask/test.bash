#!/bin/bash

#IP=${IP}
IP=http://beehive1.mcs.anl.gov

#NODE='${NODE}'
NODE='0000001e06108202'

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
    url ${IP}/admin/search/

    url ${IP}/api/
    url ${IP}/api/1/
    url ${IP}/api/1/epoch
    url ${IP}/api/1/nodes/
    url ${IP}/api/1/nodes/?all=true
fi
if true; then
    url ${IP}/api/nodes
    url "${IP}/api/1/nodes/${NODE}/dates"
    url "${IP}/api/1/nodes/${NODE}/dates?version=1"
    url "${IP}/api/1/nodes/${NODE}/dates?version=2.1"
    url "${IP}/api/1/nodes/${NODE}/dates?version=2"
    
    url "${IP}/api/nodes/${NODE}/dates"
    url "${IP}/api/nodes/${NODE}/dates?version=1"
    url "${IP}/api/nodes/${NODE}/dates?version=2.1"
    url "${IP}/api/nodes/${NODE}/dates?version=2"
fi
if true; then
    url ${IP}/api/1/nodes_last_update/
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=1"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=2.1"
    url "${IP}/api/1/nodes/${NODE}/export?date=2016-01-01&version=2"
    url ${IP}/api/1/WCC_node/${NODE}/
    
    url ${IP}/api/1/WCC_nodes_test
    url ${IP}/api/1/WCC_nodes_test?all=true
    
    url ${IP}/
    url ${IP}/wcc/test/
    url "${IP}/wcc/test/?dog=cat&tiger=lion"
    url ${IP}/wcc/
    url ${IP}/wcc/node/${NODE}/
fi
echo " "
