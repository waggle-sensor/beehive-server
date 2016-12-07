#!/usr/bin/env bash
bVerbose=false

echo "argc: " $#
echo "argv: " $*

nNodes=1
if (($# >= 1)); then
    echo "arg 1 = " $1
    nNodes=$1
fi

nDays=1
if (($# >= 2)); then
    echo "arg 2 = " $1
    nDays=$1
fi

# number of samples per day
nSamples=1
if (($# >= 3)); then
    echo "arg 3 = " $3
    nSamples=$3
fi


for ((iNode=0;iNode<$nNodes;iNode++)); do
    # create nodes
    nodeName=`printf "%016d" $iNode`
    #echo " node name = " $nodeName " #############################"
    
    # add data to nodes
    for ((iDay=1;iDay<=$nDays;iDay++)); do
        #echo "   iDay = " $iDay
        day00=`printf "%02d" $iDay`
        for ((iSample=0;iSample<$nSamples;iSample++)); do
            #echo "   iSample = " $iSample
            sample00=`printf "%02d" $iSample`

            echo " docker exec -it beehive-cassandra cqlsh -e \"USE waggle; INSERT INTO sensor_data_raw (node_id, date, ingest_id, plugin_name, plugin_version, plugin_instance, timestamp, parameter, data) VALUES ('${nodeName}', '2016-01-${day00}', 0, 'pluginName', 'pluginVersion',  'pluginInstance', '2016-01-${day00} 01:00:${sample00}', 'param', 'data')\" "
        done
    done
done
