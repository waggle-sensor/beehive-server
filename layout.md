Show docker containers
```
-bash-4.2$ docker ps
CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS              PORTS                                                                                                         NAMES
a3c70587de38        waggle/beehive-worker-coresense   "python ./worker.py"     4 weeks ago         Up 36 hours                                                                                                                       beehive-worker-coresense
622f42fef4cf        waggle/beehive-flask              "gunicorn -w 5 -b 0.0"   4 weeks ago         Up 4 weeks                                                                                                                        beehive-flask
b9f4aab8fdbb        waggle/beehive-logger             "python ./logger.py"     6 weeks ago         Up 2 days                                                                                                                         beehive-logger
ba6d39f80c01        waggle/beehive-nginx              "nginx -g 'daemon off"   4 months ago        Up 4 weeks          0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp                                                                      beehive-nginx
d31d4612ca95        waggle/beehive-plenario-sender    "python3 plenario-sen"   4 months ago        Up 3 days                                                                                                                         beehive-plenario-sender
34469543b54e        waggle/beehive-loader-raw         "python ./loader.py"     5 months ago        Up 12 hours                                                                                                                       beehive-loader-raw
b1295a350f62        waggle/beehive-sshd               "/usr/sbin/sshd -D -e"   5 months ago        Up 4 weeks          0.0.0.0:20022->22/tcp                                                                                         beehive-sshd
29d66deb57af        waggle/beehive-cert               "python ./cert-serve."   5 months ago        Up 4 weeks          127.0.0.1:24181->80/tcp                                                                                       beehive-cert
ee641aa2cac4        mysql:5.7.10                      "/entrypoint.sh mysql"   5 months ago        Up 4 weeks          127.0.0.1:3306->3306/tcp                                                                                      beehive-mysql
fdd94d0688c1        cassandra:3.2                     "/docker-entrypoint.s"   5 months ago        Up 4 weeks          7000-7001/tcp, 7199/tcp, 9160/tcp, 127.0.0.1:9042->9042/tcp                                                   beehive-cassandra
3e59e3ca8455        waggle/beehive-rabbitmq           "/docker-entrypoint.s"   5 months ago        Up 4 weeks          4369/tcp, 0.0.0.0:15671->15671/tcp, 5671/tcp, 25672/tcp, 127.0.0.1:5672->5672/tcp, 0.0.0.0:23181->23181/tcp   beehive-rabbitmq

```

Sensor Data -> Beehive's RabbitMQ data exchange

Node -> RabbitMQ
