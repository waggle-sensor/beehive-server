#!/bin/bash

# Install all of the dependencies that the Waggle server needs

set -e
set -x


export PLATFORM=`uname -i`

if [ ${PLATFORM} == "armv7l"  ]  ; then
  echo "Architecture: armv7l"
  dpkg -i packages_o/*.deb
  

elif [ ${PLATFORM} == "x86_64"  ] ; then
  echo "Architecture: x86_64"
else
  echo "Architecture not supported"
  exit 1
fi


# platform-independent python packages
pip install web.py

cd packages_o/
pip install blist
pip install cassandra-driver
pip install crcmod

cd pika-0.9.14/
python setup.py install

cd ../../
cd packages_o/
pip3 install blist
pip3 install cassandra-driver
pip3 install crcmod
pip3 install configparser

cd pika-0.10.0/
python3 setup.py install

cd ../../

# cqlshlib for the cassandra client
cd cassandra-pylib/
python ./setup.py install 

