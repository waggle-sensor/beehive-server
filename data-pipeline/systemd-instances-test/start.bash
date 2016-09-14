#!/usr/bin/env bash

echo 'hello world'

cp test@.service /etc/systemd/system

for x in `cat tests.txt`; do
   echo $x
   systemctl enable test@$x.service
   systemctl start  test@$x.service
done

sleep 3

for x in `cat tests.txt`; do
   systemctl status test@$x.service
done
