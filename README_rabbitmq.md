## RabbitMQ for Waggle


Be sure that environment variable $DATA is defined, e.g.:
```bash
export DATA="/mnt/"
```

### rabbitmq.config
```bash
mkdir -p ${DATA}/rabbitmq/config/ && \
curl https://raw.githubusercontent.com/waggle-sensor/beehive-server/master/rabbitmq/rabbitmq.config > ${DATA}/rabbitmq/config/rabbitmq.config
```

### Create SSL server certificate for RabbitMQ
```bash
docker pull waggle/beehive-server:latest

[ ! -z "$DATA" ] && docker run -ti \
  --name certs \
  --rm \
  -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
  waggle/beehive-server:latest ./SSL/create_server_cert.sh
```

### CA certificate cacert.pem
In addition to its own private key (key.pem) and certificate (cert.pem), located under /usr/lib/waggle/SSL/beehive-server, RabbitMQ also needs access to the public certificate of the CA. You can either mount that file/directory into the docker container or copy it into the container. The example below mounts the SSL directory.


### Start RabbitMQ server
```bash
docker rm -f beehive-rabbit
[ ! -z "$DATA" ] && docker run -d \
  --hostname beehive-rabbit \
  --name beehive-rabbit \
  -e RABBITMQ_NODENAME=beehive-rabbit \
  -v ${DATA}/rabbitmq/config/:/etc/rabbitmq:rw \
  -v ${DATA}/rabbitmq/data/:/var/lib/rabbitmq/:rw \
  -v ${DATA}/waggle/SSL:/usr/lib/waggle/SSL/:ro \
  --expose=5671 \
  -p 5671:5671 -p 5672:5672 \
  rabbitmq:3.5.6
```

Or, in case you have problems with file permissions on the host, you might want to call the rabbitmq-server binary directly to invoke it with root rights. Add the full path of the rabbitmq-server binary as an addtional argument to the call above.
```bash
...
rabbitmq:3.5.6 /usr/lib/rabbitmq/bin/rabbitmq-server
```

Confirm RabbitMQ is running:
```bash
docker logs beehive-rabbit
```


Create waggle user:
```bash
# old: docker exec -ti  beehive-rabbit rabbitmqctl add_user waggle waggle
# old: docker exec -ti  beehive-rabbit rabbitmqctl set_permissions waggle ".*" ".*" ".*"
docker exec -ti  beehive-rabbit rabbitmqctl add_user node waggle
docker exec -ti  beehive-rabbit rabbitmqctl add_user server waggle
docker exec -ti  beehive-rabbit rabbitmqctl set_permissions node "node_.*" ".*" ".*"
docker exec -ti  beehive-rabbit rabbitmqctl set_permissions server ".*" ".*" ".*"
```

#### Alternative installation methods for RabbitMQ:
```bash
# Ubuntu
apt-get install rabbitmq-server
```
or https://www.rabbitmq.com/download.html

