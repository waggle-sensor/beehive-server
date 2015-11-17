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

### Data directory
While services are running in containers, configuration files, SSL certificates and databases have to be stored persistently on the host. This is configured in Docker with the -v option (format: "host:container"). Depending on your system you might want to use a different location to store these files.

```bash
export DATA="/mnt"

# other examples:
# export DATA="${HOME}/waggle"
# export DATA="/media/ephemeral/"
```

### Cassandra

See [README_cassandra.md](./README_cassandra.md)

### RabbitMQ

See [README_rabbitmq.md](./README_rabbitmq.md)

### Beehive Server
If cassandra or RabbitMQ are running remotely, omit the corresponding option "--link ...".

```bash
docker run -ti --name beehive-server \
  --link beehive-cassandra:cassandra \
  --link beehive-rabbit:rabbitmq \
  waggle/beehive-server:latest
```

**Tip:** For developing purposes you can also mount the git repo into the container.
```bash
-v ${HOME}/git/beehive-server:/usr/lib/waggle/beehive-server
```

You should now be inside the container. Run the configure and Server.py scripts:
```bash
cd /beehive-server/
./configure
cd /usr/lib/waggle/beehive-server/
python ./Server.py
```
The beehive server should be running at this point. 

Leave the container and put it in background using key combinations "Ctrl-P" "Ctrl-Q". You can re-attach to the container with
```bash
docker attach beehive-server
```
or enter the container without attaching to the main process (python Server.py) with "docker exec":
```bash
docker exec -ti beehive-server bash
```

