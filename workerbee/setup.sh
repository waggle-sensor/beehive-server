#!/bin/bash

basedir=$(pwd $(dirname $0))

cd $basedir
python3 -m venv waggle-python
source waggle-python/bin/activate && pip install -r requirements.txt
