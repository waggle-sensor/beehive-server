#!/bin/sh

for image in $(echo beehive-*); do
  cd $image
  make deploy
  cd ..
done
