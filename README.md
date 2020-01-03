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

## Deployment Instructions

```
git clone https://github.com/waggle-sensor/beehive-server
cd beehive-server
```

### Deploy Containers

Next, we'll specify a deployment directory and spin up all the containers. The deployment directory holds 

1. Databases 
2. Nodes Keys 
3. Beehive Keys 
4. RMQ data

If you remove this directory you loose all persistent stuff. The incoming data from the nodes also gets stored under this directory.

```
export BEEHIVE_ROOT=/path/to/deploy/into
./do.sh deploy
```

### Perform Initial Setup of Containers

Now, we perform some one-time configuration of our containers:

```
./do.sh setup
```

You should be prompted for a RabbitMQ server admin password during this
process. Remember to choose this password wisely. You can always rerun
this step if you forget the password.


