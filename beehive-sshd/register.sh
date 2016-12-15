#!/bin/bash

cert_server_ip=beehive-cert

api_call=${SSH_ORIGINAL_COMMAND}
if [[ $api_call == "" || $api_call == "certca" || $api_call == "node?"* ]]; then
  curl -s "$cert_server_ip/$api_call"
fi

