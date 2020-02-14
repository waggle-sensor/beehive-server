#!/bin/bash

export BEEHIVE_ROOT=$PWD/beehive-root/

./do.sh cleanup
rm -rf $BEEHIVE_ROOT
sleep 10
./do.sh deploy
sleep 30
echo secret | ./do.sh setup
sleep 30
(cd beehive-nginx; ./update_nginx_config.sh)
