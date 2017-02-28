#!/bin/bash

# this script requires bash version 4

# Delete 'exited' and ‘created’ containers and their associated volumes
docker rm -v $(docker ps -a -q -f status=exited -f status=created)

# Delete 'dangling' images
docker rmi $(docker images -f "dangling=true" -q)

# Delete 'dangling' volumes
docker volume rm $(docker volume ls -qf dangling=true)


# WCC: I don't know if this (below) is obsolete given the above (new) commands
if false; then
    # get list of (tagged) images that are used by running containers
    declare -A usedimages
    for i in $(docker ps | awk '{ print $2; }' | grep -v "^ID$") ; do ID=$(docker inspect  --format="{{.Id}}" $i) ; usedimages[$ID]=$i ; done

    for i in "${!usedimages[@]}"
    do
      echo "key  : $i"
      echo "value: ${usedimages[$i]}"
    done


    # delete all unused (tagged) images
    for i in $(docker images --no-trunc -q | sort -u) 
      do
      if [[ ${usedimages[$i]}x != "x" ]] ; then
        echo "image is used: $i"
        echo "by ${usedimages[$i]}"
      else
        echo "image is not used: $i"
        docker rmi $i
      fi
    done
fi
