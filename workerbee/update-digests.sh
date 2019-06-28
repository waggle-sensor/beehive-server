#!/bin/bash

source /homes/moose/workerbee/waggle-env.sh

python3 /homes/moose/workerbee/generate-expected-keys-for-projects.py /homes/moose/workerbee/beehive-server/publishing-tools/projects/*.complete/nodes.csv > /tmp/datasets-v1-expect

if list-datasets > /tmp/datasets-v1.new; then
  mv /tmp/datasets-v1.new /tmp/datasets-v1
fi

if list-datasets-v2 > /tmp/datasets-v2.new; then
  mv /tmp/datasets-v2.new /tmp/datasets-v2
fi

function cleanup() {
  find $DIGESTS_DIR -type d -name '*.20*' | grep -v $(date +'%Y-%m-%d') | xargs rm -rf
  find $DIGESTS_DIR -name '2036-*.csv.gz' | xargs rm
  find $DATASETS_DIR -name '2036*.csv.gz' | xargs rm
}

function compile() {
  # export any remaining items just before exporting
  sort -u /tmp/datasets-v1 /tmp/datasets-v1-expect | filter-last-3-days | export-datasets -p 4 $DATASETS_DIR
  find $DATASETS_DIR -name '2036*.csv.gz' | xargs rm

  filter-last-3-days < /tmp/datasets-v2 | export-datasets-v2 $DATASETS_DIR_V2 /homes/moose/workerbee/sdf.csv /homes/moose/workerbee/plugin_manager/plugins/*.plugin

  for p in $(ls $PROJECTS_DIR | grep .complete); do
    echo "compile $p -- complete"
    compile-digest-v2 --complete -p 4 --data $DATASETS_DIR --data $DATASETS_DIR_V2 $DIGESTS_DIR/$p/ $PROJECTS_DIR/$p
  done

  for p in $(ls $PROJECTS_DIR | grep -v .complete); do
    echo "compile $p"
    compile-digest-v2 -p 4 --data $DATASETS_DIR --data $DATASETS_DIR_V2 $DIGESTS_DIR/$p/ $PROJECTS_DIR/$p
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
