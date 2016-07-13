#!/bin/bash

# this script requires bash version 4

#delete all stopped containers
docker rm $(docker ps -f status=exited -q)


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

