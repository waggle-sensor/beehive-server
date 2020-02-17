#!/bin/sh
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

set -e

do_deploy() {
  mkdir -p $BEEHIVE_ROOT/ssh_keys
  cp ssh/id_rsa_waggle_aot_registration.pub $BEEHIVE_ROOT/ssh_keys/

  do_build

  do_deploy_only

  # Run setup only once
  if [  ! -e ${BEEHIVE_ROOT}/setup_success.flag ] ; then
    do_setup
    touch ${BEEHIVE_ROOT}/setup_success.flag
  fi

}

do_setup() {
  for image in $(echo beehive-*); do
    # skip Makefile if target is missing anyway
    if ! grep --quiet '^setup:' $image/Makefile ; then
      continue
    fi
      
    echo "setup $image ..."
    cd $image
    make setup
    cd ..
    
  done
}


do_deploy_only() {
  
  for image in $(echo beehive-*); do
    echo "deploying $image ..."
    cd $image
    make deploy
    cd ..
  done

}


do_build() {

  for image in $(echo beehive-*); do
    echo "building $image ..."
    cd $image
    make build
    cd ..
  done

}


do_cleanup() {
  GLOBIGNORE=beehive-core
  set -x
  docker rm -f  beehive-*
  set +x
  unset GLOBIGNORE
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
  test)
    python3 -m unittest discover -s tests
    ;;
  *)
    echo "Usage: do.sh (deploy|setup|cleanup|test)"
    exit 1
    ;;
esac
