#!/bin/bash

source /home/sean/waggle-recent-env.sh

function cleanup() {
  find $DIGESTS_DIR -type d -name '*.20*' | grep -v $(date +'%Y-%m-%d') | xargs rm -rf
  find $DIGESTS_DIR -name '2036-*.csv.gz' | xargs rm
  find $DATASETS_DIR -name '2036*.csv.gz' | xargs rm
}

function compile() {
  for p in $(ls $PROJECTS_DIR | grep .complete); do
    echo "compile $p -- complete"
    compile-digest --complete -p 8 $DATASETS_DIR $DIGESTS_DIR/$p/ $PROJECTS_DIR/$p
  done

  for p in $(ls $PROJECTS_DIR | grep -v .complete); do
    echo "compile $p"
    compile-digest -p 8 $DATASETS_DIR $DIGESTS_DIR/$p/ $PROJECTS_DIR/$p
  done
}

function upload() {
  target='aotpub:/mcs/www.mcs.anl.gov/research/projects/waggle/downloads/datasets'

  for p in $(ls $DIGESTS_DIR); do
    gzip -dfk $DIGESTS_DIR/$p/data.csv.gz
    src=$DIGESTS_DIR/$p/data.csv
    dst=$target/$p.recent.csv
    scp $src $dst

    src=$DIGESTS_DIR/$p/$p.latest.tar
    dst=$target/$p.recent.tar
    scp $src $dst
  done
}

#cleanup
compile
upload
