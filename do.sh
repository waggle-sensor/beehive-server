#!/bin/sh
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

do_deploy() {
  mkdir -p $BEEHIVE_ROOT/ssh_keys
  cp ssh/id_rsa_waggle_aot_registration.pub $BEEHIVE_ROOT/ssh_keys/

  for image in $(echo beehive-*); do
    cd $image
    make build
    cd ..
  done

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
