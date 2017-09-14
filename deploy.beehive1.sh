#!/bin/sh

for image in $(echo beehive-*); do
  cd $image
  make -f Makefile.beehive1 deploy
  cd ..
done
