#!/bin/bash
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

source /home/sean/waggle-env.sh

function cleanup() {
  find $DIGESTS_DIR -type d -name '*.20*' | grep -v $(date +'%Y-%m-%d') | xargs rm -rf
  find $DIGESTS_DIR -name '2036-*.csv.gz' | xargs rm
  find $DATASETS_DIR -name '2036*.csv.gz' | xargs rm
}

function compile() {
  for p in $(ls $PROJECTS_DIR | grep .complete); do
    echo "compile $p -- complete"
    compile-digest --complete -p 4 $DATASETS_DIR $DIGESTS_DIR/$p/ $PROJECTS_DIR/$p
  done

  for p in $(ls $PROJECTS_DIR | grep -v .complete); do
    echo "compile $p"
    compile-digest $DATASETS_DIR $DIGESTS_DIR/$p/ $PROJECTS_DIR/$p
  done
}

function upload() {
  for p in $(ls $DIGESTS_DIR); do
    src=$DIGESTS_DIR/$p/$p.latest.tar
    dst=aotpub:/mcs/www.mcs.anl.gov/research/projects/waggle/downloads/datasets/$p.latest.tar
    scp $src $dst
  done
}

cleanup
compile
upload
