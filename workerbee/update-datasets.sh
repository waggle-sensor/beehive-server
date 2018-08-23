#!/bin/bash

source /home/sean/waggle-env.sh

function cleanup {
  ssh beehive1-proxy -O stop
}

ssh -O check beehive1-proxy || ssh -fN beehive1-proxy
trap cleanup EXIT

list-datasets | filter-last-day | export-datasets -p 8 $DATASETS_DIR
find $DATASETS_DIR -name '2036*.csv.gz' | xargs rm
