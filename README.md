# Beehive Server

Waggle cloud software for aggregation, storage and analysis of sensor data from Waggle nodes

## Installation

The recommended installation method for the waggle beehive server is Docker. But it should be easily possible to install everything in a non-virtualized ubuntu environment. In that case we recommend ubuntu trusty (14.04). If you are using Docker, you can use any operating system with a recent Linux kernel that runs Docker. 

**NOTE:** (WCC 2/13/2017) We will assume that beehive is installed on Ubuntu.  LastSsh.py assumes python3 is available from the host command line.  Others may follow.

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

### MySQL

See [beehive-mysql/README.md](./beehive-mysql/README.md)

### RabbitMQ

See [beehive-rabbitmq/README.md](./beehive-rabbitmq/README.md)

### Beehive Server (with Docker)
```bash
docker pull waggle/beehive-server:latest
```


#### Client certificate for beehive server
```bash
[ ! -z "$DATA" ] && docker run -ti \
  --name certs \
  --rm \
  -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
  waggle/beehive-server:latest ./SSL/create_client_cert.sh server beehive-server
```  


#### Starting the docker container
If cassandra or RabbitMQ are running remotely, omit the corresponding option "--link ..." and configure /etc/waggle/beehive-server.cfg accordingly.

```bash
docker rm -f beehive-server
docker pull waggle/beehive-server
docker run -ti --name beehive-server \
  --net beehive \
  -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
  waggle/beehive-server:latest
```

You should now be inside the container.

**Tip:** For developing purposes you can also mount the git repo into the container.
```bash
-v ${HOME}/git/beehive-server:/usr/lib/waggle/beehive-server
```


#### Configure the beehive server

You can set RabbitMQ and Cassandra hostnames in /etc/waggle/beehive-server.cfg if they are installed remotely. The configure script will create this file if it does not yet exist. 

Run configure script.
```bash
./configure
```

#### Start the server.
```bash
./Server.py [--logging]
```

The beehive server should be running at this point. 

If you are in a Docker container, leave the container and put it in background using key combinations "Ctrl-P" "Ctrl-Q". You can re-attach to the container with
```bash
docker attach beehive-server
```
or enter the container without attaching to the main process (Server.py) with "docker exec":
```bash
docker exec -ti beehive-server /bin/bash
```

### Beehive Server (without Docker)
If you are not using a Docker container you can install dependencies with this script.
```bash
./install_dependencies.sh
```

Client certificate for beehive server
```bash
./SSL/create_client_cert.sh server beehive-server
```

Configure
```bash
./configure
```

Start the server.
```bash
./Server.py [--logging]
```

#### Build beehive-server Docker image

If you want to build the docker image on your own:

```bash
docker rm -f beehive-server
docker rmi waggle/beehive-server
docker build -t waggle/beehive-server .
```


## Systemd

To use systemd unit files for the beehive components, follow these instructions:


[systemd/README.md](./systemd/README.md)

## TroubleShooting

### SSL certificate related problems

If a node gets the error below when the node tries to connect to the beehive server, the SSL certificate key that the node is using may possibly be wrong or corrupted. 

```
# log from node side
2016-06-28 22:34:29,260 - __main__ - ERROR - line=312 - Could not connect to Beehive server (xxx.xxx.xxx.xxx): Connection to xxx.xxx.xxx.xxx:yyyyy failed: [Errno 1] _ssl.c:510: error:0407006A:rsa routines:RSA_padding_check_PKCS1_type_1:block type is not 01
```

When it happens you may need to re-generate certificate from the server side by following the instruction [certificate for rabbitmq](beehive-rabbitmq/README.md#create-ssl-server-certificate-for-rabbitmq). At the same time, the node should also get rid of the existing certificates and restart waggle-communications service,

```bash
# in the node terminal
cd /usr/lib/waggle
rm -rf SSL
waggle-service stop waggle-communications
waggle-service start waggle-communications
```
