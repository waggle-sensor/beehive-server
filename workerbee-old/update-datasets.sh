#!/bin/bash
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

source /home/sean/waggle-env.sh

function cleanup {
  ssh beehive1-proxy -O stop
}

ssh -O check beehive1-proxy || ssh -fN beehive1-proxy
trap cleanup EXIT

list-datasets | filter-last-day | export-datasets -p 8 $DATASETS_DIR
find $DATASETS_DIR -name '2036*.csv.gz' | xargs rm
