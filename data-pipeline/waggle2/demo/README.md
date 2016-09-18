# How to Use Waggle Data
Get the program wag.py Using
```
wget github.com/
```
Using python3, import the necessary libraries.
```
pip3 install pandas
pip3 install bokeh
```
from terminal 1 - run
bokeh serve

We'll leave that terminal.
Start a new one.


    load_csv
        change pd.read_csv to requests() to get data
        load_data reads data from beehive1 in old format
        I'll add a function to convert to the new format


To get

# Beehive Server

Waggle cloud software for aggregation, storage and analysis of sensor data from Waggle nodes

## Installation

The recommended installation method for the waggle beehive server is Docker. But it should be easily possible to install everything in a non-virtualized ubuntu environment. In that case we recommend ubuntu trusty (14.04). If you are using Docker, you can use any operating system with a recent Linux kernel that runs Docker.

### Docker

To get the latest version of Docker in Ubuntu use this (simply copy-paste the whole block):
```
apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
export CODENAME=$(lsb_release --codename | grep -o "[a-z]*$" | tr -d '\n')
echo "deb https://apt.dockerproject.org/repo ubuntu-${CODENAME} main" > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install -y  docker-engine
```

### Data directory
While services are running in containers, configuration files, SSL certificates and databases have to be stored persistently on the host. This is configured in Docker with the -v option (format: "host:container"). Depending on your system you might want to use a different location to store these files.

```bash
export DATA="/mnt"

# other examples:
# export DATA="${HOME}/waggle"
# export DATA="/media/ephemeral/"
```

It might be helful to set this variable permanently. For example, if you are using bash:
```bash
echo "export DATA=/mnt/" >> ~/.bash_profile
```

### Docker network
Docker network provides a mechanism for service discovery. To us it create the network "beehive":
```bash
docker network create beehive
```

To verify these command can be used:
```bash
docker network ls
docker network inspect beehive
```

### SSL certificates

Create certificate authority:

See [SSL/README.md](./SSL/README.md)

### Cassandra

See [beehive-cassandra/README.md](./beehive-cassandra/README.md)
