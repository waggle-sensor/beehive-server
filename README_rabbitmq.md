### RabbitMQ


Be sure that environment variable $DATA is defined.


Download rabbitmq.config
```bash
mkdir -p ${DATA}/rabbitmq/config/
curl https://raw.githubusercontent.com/waggle-sensor/beehive-server/master/SSL/rabbitmq.config > ${DATA}/rabbitmq/config/rabbitmq.config
```

Create server certificates
```bash
docker run -ti \
--name certs \
--rm \
-v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
waggle/beehive-server:latest ./scripts/configure_ssl.sh
```

Start RabbitMQ server
```bash
docker run -d \
--hostname beehive-rabbit \
--name beehive-rabbit \
-e RABBITMQ_NODENAME=beehive-rabbit \
-v ${DATA}/rabbitmq/config/:/etc/rabbitmq:ro \
-v ${DATA}/rabbitmq/data/:/var/lib/rabbitmq/:rw \
-v ${DATA}/waggle/SSL:/usr/lib/waggle/SSL/ \
-p 5671:5671 \
rabbitmq:3.5.6
```

Or, in case you have problems with file permissions on the host, you might want to call the rabbitmq-server binary directly to invoke it with root rights. Add the full path of the rabbitmq-server binary as an addtional argument to the call above.
```bash
...
rabbitmq:3.5.6 /usr/lib/rabbitmq/bin/rabbitmq-server
```

Create waggle user:
```bash
docker exec -ti  beehive-rabbit rabbitmqctl add_user waggle waggle
docker exec -ti  beehive-rabbit rabbitmqctl set_permissions waggle ".*" ".*" ".*"
```

#### Alternative installation methods for RabbitMQ:
```bash
# Ubuntu
apt-get install rabbitmq-server
```
or https://www.rabbitmq.com/download.html

