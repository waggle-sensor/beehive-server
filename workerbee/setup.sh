#!/bin/bash

basedir=$(pwd $(dirname $0))

cd $basedir

git clone https://github.com/waggle-sensor/beehive-server
git clone https://github.com/waggle-sensor/plugin_manager

python3 -m venv waggle-python
source waggle-python/bin/activate && pip install -r requirements.txt
