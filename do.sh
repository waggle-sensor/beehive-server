#!/bin/sh

do_deploy() {
  for image in $(echo beehive-*); do
    cd $image
    make deploy
    cd ..
  done
}

do_setup() {
  for image in $(echo beehive-*); do
    cd $image
    make setup
    cd ..
  done
}

do_cleanup() {
  docker rm -f $(echo beehive-*)

  rm -rf \
    $BEEHIVE_ROOT/cassandra \
    $BEEHIVE_ROOT/log \
    $BEEHIVE_ROOT/mysql \
    $BEEHIVE_ROOT/rabbitmq waggle
}

if [ -z "$BEEHIVE_ROOT" ]; then
  echo "Environment variable BEEHIVE_ROOT is required."
  exit 1
fi

case $1 in
  deploy)
    do_deploy
    ;;
  setup)
    do_setup
    ;;
  cleanup)
    do_cleanup
    ;;
  *)
    echo "Usage: do.sh (deploy|setup|cleanup)"
    exit 1
    ;;
esac
