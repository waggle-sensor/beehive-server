#!/bin/bash

until [ $(docker inspect -f {{.State.Running}} beehive-cert)_ == "true_" ]; do
    echo "waiting for beehive-cert..."
    sleep 1
done