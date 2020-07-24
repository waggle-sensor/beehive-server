#!/bin/bash


if [ ! -e ./do.sh ] ; then
  echo "Please strat this script from the root of the beehive-server git repository"
  exit 1
fi


if [ -z "$BEEHIVE_ROOT" ]; then
  echo "Environment variable BEEHIVE_ROOT is not defined, using ${PWD}/data/"
  export BEEHIVE_ROOT=${PWD}/data/
  sleep 1
fi


if [ $(ls -1q 2>/dev/null  ${BEEHIVE_ROOT}/ssh_keys/beehive-registration-key* | wc -l) -ne 0 ] ; then
  echo "Existing files found!"
  echo "Please delete existing files, e.g. \"rm ${BEEHIVE_ROOT}/ssh_keys/beehive-registration-key*\""
  exit 1
fi

set -x

ssh-keygen -f ${BEEHIVE_ROOT}/ssh_keys/beehive-registration-key -N ''

set +x