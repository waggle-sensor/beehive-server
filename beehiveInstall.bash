#!/bin/bash
# Must be run after superuser -i command:
### sudo -i

#####################################################################
#########   UN-INSTALL old beehive server
#####################################################################

## files in $DATE=/mnt
rm -rf /mnt/cassandra  /mnt/mysql  /mnt/rabbitmq  /mnt/ssh_keys  /mnt/waggle

##-- systemd
cd /etc/systemd/system
systemctl stop beehive-*
systemctl disable beehive-*
rm -f /etc/systemd/system/beehive-*.service

systemctl status beehive-*  --no-pager -l
systemctl list-units beehive-* --all

##-- docker containers
echo "BEFORE removal...."
docker ps
for container in `docker ps -q`;
do echo ' removing container ' $container
   docker rm -fv $container
done
echo "AFTER removal...."
docker ps
echo "...."


#####################################################################
#########   INSTALL
#####################################################################

#### Docker

apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
export CODENAME=$(lsb_release --codename | grep -o "[a-z]*$" | tr -d '\n')
echo "deb https://apt.dockerproject.org/repo ubuntu-${CODENAME} main" > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install -y  docker-engine

export DATA="/mnt"
echo "export DATA=/mnt/" >> ~/.bash_profile
docker network create beehive

docker network ls
docker network inspect beehive

### SSL
docker pull waggle/beehive-server:latest

[ ! -z "$DATA" ] && docker run -ti \
  --name certs \
  --rm \
  -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
  waggle/beehive-server:latest ./SSL/create_certificate_authority.sh

### Cassandra
[ ! -z "$DATA" ] && \
docker run -d \
--name beehive-cassandra \
--net beehive \
-v ${DATA}/cassandra/:/var/lib/cassandra/ \
--ulimit memlock=-1 \
--ulimit nofile=100000 \
--ulimit nproc=32768 \
--cap-add IPC_LOCK \
cassandra:3.2 -R

### RabbitMQ
apt-get install curl
mkdir -p ${DATA}/rabbitmq/config/ && \
curl https://raw.githubusercontent.com/waggle-sensor/beehive-server/master/beehive-rabbitmq/rabbitmq.config > ${DATA}/rabbitmq/config/rabbitmq.config

docker pull waggle/beehive-server:latest

[ ! -z "$DATA" ] && docker run -ti \
  --name certs \
  --rm \
  -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
  waggle/beehive-server:latest ./SSL/create_server_cert.sh

chmod +x ${DATA}/waggle/SSL/server

docker rm -f beehive-rabbitmq
[ ! -z "$DATA" ] && docker run -d \
  --hostname beehive-rabbitmq \
  --name beehive-rabbitmq \
  -e RABBITMQ_NODENAME=beehive-rabbitmq \
  -v ${DATA}/rabbitmq/config/:/etc/rabbitmq:rw \
  -v ${DATA}/rabbitmq/data/:/var/lib/rabbitmq/:rw \
  -v ${DATA}/waggle/SSL:/usr/lib/waggle/SSL/:ro \
  --expose=23181 \
  -p 23181:23181 \
  --net beehive \
  rabbitmq:3.5.6

docker logs beehive-rabbitmq

docker exec -ti  beehive-rabbitmq bash -c '\
    rabbitmqctl add_user node waggle  ; \
    rabbitmqctl add_user server waggle  ; \
    rabbitmqctl set_permissions node "node_.*" ".*" ".*"  ; \
    rabbitmqctl set_permissions server ".*" ".*" ".*"  ; \
    rabbitmq-plugins enable rabbitmq_auth_mechanism_ssl'

### Beehive Server (with Docker)
docker pull waggle/beehive-server:latest

[ ! -z "$DATA" ] && docker run -ti \
  --name certs \
  --rm \
  -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
  waggle/beehive-server:latest ./SSL/create_client_cert.sh server beehive-server

###--- Starting the docker container
docker rm -f beehive-server
docker pull waggle/beehive-server
#docker run -ti --name beehive-server \
docker run -tid --name beehive-server \
  --net beehive \
  -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
  waggle/beehive-server:latest

docker exec beehive-server    ls configure Server.py
docker exec beehive-server    ./configure
docker exec -d beehive-server    ./Server.py --logging

### systemd  
cd ~
rm -rf git
mkdir -p git
cd git
git clone https://github.com/waggle-sensor/beehive-server.git
cd ~/git/beehive-server/systemd/
  
for service in *.service ; do
  echo "Deploy ${service}"
  rm -f /etc/systemd/system/${service}
  cp ${service} /etc/systemd/system
  systemctl enable ${service}
  systemctl start ${service}
  sleep 3
  systemctl status ${service}  --no-page -l
done
#systemctl status beehive-*  --no-page -l
