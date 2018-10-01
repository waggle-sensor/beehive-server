#!/bin/bash

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
