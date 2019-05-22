# Installation Instructions

These instructions assume a few things about your target computer:

1. The host operating system is Ubuntu 18.04
2. The computer has internet access
3. You have either root access or sudo privileges (this guide assumes sudo)


## Install Docker

This is lifted from https://docs.docker.com/install/linux/docker-ce/ubuntu/ as of May 2019. You may want to review Docker's official documentation rather than rely on this.

```bash
# make sure you don't have an old version installed
sudo apt remove docker docker-engine docker.io containerd runc

# install dependencies
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

# add the docker key and repo
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# update your cache and install
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# ensure docker starts on boot
sudo systemctl enable docker

# ensure docker is working
sudo docker run hello-world
```


## Set the BEEHIVE_ROOT Env Var

We want to persist the env var for all sessions, so we're going to update the system environment file.

**WARNING:** make sure that the path you set is sufficiently large enough to handle the volume of data that will be stored there, and that it is a permanently mapped/mounted disk. This file system will include the database, keys and RabbitMQ data.

```bash
echo 'BEEHIVE_ROOT=/mnt/storage' | sudo tee -a /etc/environment

# you'll have to do this and log back in to refresh the environment
exit
```

**NOTE:** we are using a generic `/mnt/storage` location -- yours might be different depending on how you configured your host system.


## Clone the Beehive Repo

You're going to need to ensure git is installed first.

```bash
sudo apt install git
```

Next, cd into BEEHIVE_ROOT and clone the repo.

```bash
cd $BEEHIVE_ROOT
sudo git clone https://github.com/waggle-sensor/beehive-server.git
```


## Build, Run and Configure the Services

The final step is to build, run and configure the services. It must be run in this order -- you can only configure running services.

First, cd into the cloned repo.

```bash
cd beehive-server
```

Then run the make targets.

```bash
make build
make run
make configure
```


## Getting Help

From either the project root or in each of the service configuration directories (prefixed with _beehive-_) you can run `make help` to pull up usage information about the actions that are available to you.

From the project root you have the following actions available:

- `make build` will build the images for the services
- `make run` will start the containers from the built images for the services
- `make configure` will run the setup/init scripts for the services (if available -- not all require configuration beyond building their image)
- `make stop` will stop all the service
- `make snapshot` will create tags for all the images with the current date so that you can rebuild, run, and roll back if need be.
