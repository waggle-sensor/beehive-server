#!/bin/bash

source /home/sean/waggle-recent-env.sh

function cleanup {
  ssh beehive1-proxy -O stop
}

ssh -O check beehive1-proxy || ssh -fN beehive1-proxy
trap cleanup EXIT

# rm -rf $DATASETS_DIR
list-datasets | filter-last-day | export-recent-datasets --since 1800 -p 8 $DATASETS_DIR
