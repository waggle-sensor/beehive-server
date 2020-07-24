<!--
waggle_topic=/beehive/introduction
-->

# Beehive Server


Beehive Server is a set of services that collect sensor data from Waggle IoT devices.


For an overview of Waggle visit [https://wa8.gl/](https://wa8.gl/)



## System Requirements

- OS: Linux, OSX
- Software: Make, Docker

### Docker

We'll assume Docker CE (Community Edition) version 17.01 or later (_check minimal version_) is installed on the system. 

Installation guides for Docker [https://docs.docker.com/install/)](https://docs.docker.com/install/)

## Installation

```
git clone https://github.com/waggle-sensor/beehive-server
cd beehive-server
```

Optional: The default location for persistent data is the `data` subfolder. If you want to change this, define the `BEEHIVE_ROOT`. See next section for documentation.
```bash
export BEEHIVE_ROOT=`pwd`/beehive-server
```

To be able to connect a virtual or real waggle nodes to beehive, create a registration key:
```bash
./scripts/create_registration_key.sh 
```

```bash
./do.sh deploy
```



### BEEHIVE_ROOT: Persistent data

By default all your beehive data be stored in a `data/` subfolder in your checked out git repository. This data directory will contain:

1. Databases 
2. Nodes Keys 
3. Beehive Keys 
4. RMQ data

If you remove this directory you loose all persistent stuff. The incoming data from the nodes also gets stored under this directory.

To change location of your data folder, set the `BEEHIVE_ROOT` variable, e.g.

```bash
export BEEHIVE_ROOT=${HOME}/beehive-server-data
```

(Pro tip: store the beehive variable in you ~/.bashrc or similar)

