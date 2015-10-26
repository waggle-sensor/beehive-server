# Beehive Server

Waggle cloud software for aggregation, storage and analysis of sensor data from Waggle nodes

## Installation

The recommended installation method for the waggle beehive server is Docker. But it should be easily possible to install everything in a non-virtualized ubuntu environment. In that case we recommend ubuntu trusty (14.04). If you are using Docker, you can use any operating system with a recent Linux kernel that runs Docker. 

### Docker

To get the latest version of Docker in Ubuntu use this (simply copy-paste the whole block):
```
apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
export CODENAME=$(lsb_release --codename | grep -o "[a-z]*$" | tr -d '\n')
echo "deb https://apt.dockerproject.org/repo ubuntu-${CODENAME} main" >> /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install -y  docker-engine
```

### Cassandra:
```bash
docker run -d --name beehive-cassandra -v /mnt/cassandra/data/:/var/lib/cassandra/data cassandra:2.2.3
```
You may want to change the -v option (format: "host:container") to point to file system location with sufficient space for the Cassandra database files.

Installation instructions for Cassandra without Docker:

http://docs.datastax.com/en/cassandra/2.0/cassandra/install/installDeb_t.html

### Beehive Server
This requires that the cassandra container is already running on the same machine. If cassandra is running remotely, do not use option "--link ...".

```bash
docker run -ti --name beehive-server --link beehive-cassandra:cassandra waggle/beehive-server:latest
```

Inside the container:
```bash
cd /beehive-server/
./configure
cd /usr/lib/waggle/beehive-server/
python /usr/lib/waggle/beehive-server/Server.py &
```
Leave container and put it in background with "Ctrl-P" "Ctrl-Q".

## Developer Notes

TODO: Run RabbitMQ in its own container.

