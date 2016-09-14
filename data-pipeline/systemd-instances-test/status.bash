#!/usr/bin/env bash

for x in `cat tests.txt`; do
   echo $x
   systemctl status test@$x.service
done
