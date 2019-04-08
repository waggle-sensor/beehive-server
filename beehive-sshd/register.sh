#!/bin/bash
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

cert_server_ip=beehive-cert

run_command() {
  case $1 in
    cacert)
      curl -s "$cert_server_ip/certca"
      ;;
    certca)
      curl -s "$cert_server_ip/certca"
      ;;
    node?*)
      curl -s "$cert_server_ip/$1"
      ;;
    epoch)
      date +%s
      ;;
    *)
      echo "invalid command"
      exit 1
      ;;
  esac
}

run_command "$SSH_ORIGINAL_COMMAND"
