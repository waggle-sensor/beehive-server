#!/bin/sh

for image in $(echo beehive-*); do
  cd $image
  make build
  cd ..
done
