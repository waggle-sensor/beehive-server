#!/bin/bash

source /homes/moose/workerbee/waggle-recent-env.sh

#python /homes/moose/workerbee/generate-expected-keys.py > /tmp/datasets-recent-v1-known
python /homes/moose/workerbee/generate-expected-recent-keys-for-projects.py /homes/moose/workerbee/beehive-server/publishing-tools/projects/*.complete/nodes.csv > /tmp/datasets-recent-v1-expect

# ensure that we only use a clean dataset list. fallback to cached on failure.
if list-datasets > /tmp/datasets-recent-v1.new; then
  mv /tmp/datasets-recent-v1.new /tmp/datasets-recent-v1
fi

if list-datasets-v2 > /tmp/datasets-recent-v2.new; then
  mv /tmp/datasets-recent-v2.new /tmp/datasets-recent-v2
fi

function cleanup() {
  find $DIGESTS_DIR -type d -name '*.20*' | grep -v $(date +'%Y-%m-%d') | xargs rm -rf
  find $DIGESTS_DIR -name '2036-*.csv.gz' | xargs rm
  find $DATASETS_DIR -name '2036*.csv.gz' | xargs rm
}

function compile() {
  rm -rf $DATASETS_DIR $DATASETS_DIR_V2 $DIGESTS_DIR

  # export datasets now. need to check if this succeeds
  sort -u /tmp/datasets-recent-v1 /tmp/datasets-recent-v1-expect | filter-last-day | export-recent-datasets --since 1800 -p 4 $DATASETS_DIR
  filter-last-day < /tmp/datasets-recent-v2 | export-recent-datasets-v2 --since 1800 $DATASETS_DIR_V2 /homes/moose/workerbee/sdf.csv /homes/moose/workerbee/plugin_manager/plugins/*.plugin

  for p in $(ls $PROJECTS_DIR | grep .complete); do
    echo "compile $p -- complete"
    compile-digest-v2 --no-cleanup --complete -p 4 --data $DATASETS_DIR --data $DATASETS_DIR_V2 $DIGESTS_DIR/$p/ $PROJECTS_DIR/$p
  done

  for p in $(ls $PROJECTS_DIR | grep -v .complete); do
    echo "compile $p"
    compile-digest-v2 --no-cleanup -p 4 --data $DATASETS_DIR --data $DATASETS_DIR_V2 $DIGESTS_DIR/$p/ $PROJECTS_DIR/$p
  done
}

function upload() {
  target='aotpub:/mcs/www.mcs.anl.gov/research/projects/waggle/downloads/datasets'

  for p in $(ls $DIGESTS_DIR); do
    echo "upload $p - start"
    gzip -c -d $DIGESTS_DIR/$p/data.csv.gz > $DIGESTS_DIR/$p/data.csv
    src=$DIGESTS_DIR/$p/data.csv
    dst=$target/$p.recent.csv
    scp $src $dst

    src=$DIGESTS_DIR/$p/$p.latest.tar
    dst=$target/$p.recent.tar
    if scp $src $dst; then
      echo "upload $p - done"
    else
      echo "upload $p - error"
    fi
  done
}

start_compile_time=$(date +%s)
compile
end_compile_time=$(date +%s)

start_upload_time=$(date +%s)
upload
end_upload_time=$(date +%s)

node_total=$(ls /storage/recent/datasets | wc -l)
data_total=$(find /storage/recent/datasets -name '*.csv.gz' | xargs gzip -c -d | wc -l)
data_bytes=$(du -b /storage/recent/datasets | tail -n 1 | cut -f 1)

query_partition_keys_time=$(stat -c %Y /tmp/datasets-recent-v1 || echo 0)

(
echo waggle_recent_query_partition_keys_seconds $query_partition_keys_time
echo waggle_recent_compile_start_time_seconds $start_compile_time
echo waggle_recent_compile_end_time_seconds $end_compile_time
echo waggle_recent_upload_start_time_seconds $start_upload_time
echo waggle_recent_upload_end_time_seconds $end_upload_time
echo waggle_recent_node_total $node_total
echo waggle_recent_data_total $data_total
echo waggle_recent_data_bytes $data_bytes
echo waggle_recent_window_seconds 1800
) > /storage/metrics/waggle.prom.$$ && mv /storage/metrics/waggle.prom.$$ /storage/metrics/waggle.prom
