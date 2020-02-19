#!/bin/bash

export BEEHIVE_ROOT=$PWD/data

./do.sh cleanup

# BE VERY CAREFUL ABOUT CHANGING THIS rm!
# You don't want to allow this to wipe a sensitive directory!
rm -rf $BEEHIVE_ROOT

./do.sh deploy
