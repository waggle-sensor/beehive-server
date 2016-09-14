#!/usr/bin/env bash

echo 'goodbye cruel world'

for x in `cat tests.txt`; do
   echo $x
   systemctl stop    test@$x.service
   systemctl disable test@$x.service
done

sleep 2

for x in `cat tests.txt`; do
   systemctl status  test@$x.service
done
