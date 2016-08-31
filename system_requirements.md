
#System requirement for beehive1.mcs.anl.gov


## beehive1

```text
4 CPUs
16GB RAM (can be less without cassandra)
40 GB disk space
```

Ports
```text
80 : nginx: web (world-wide) and API (world-wide)
22 : ssh (ANL only)
20022 : ssh, reverse ssh tunnel for the nodes (world-wide)
23181 : RabbitMQ (world-wide)
24181 : certificate server (ANL only)
```


## cassandra cluster
(3 instances each)

```text
16 GB RAM
40 GB disk space
```

Ports:
```text
80 : web (ANL only)
22 : ssh (ANL only)

23181 : RabbitMQ (for testing)
23182 : RabbitMQ (for cluster communication testing)

7000 : cassandra cluster communication
7001 : cassandra cluster communication using ssl
```



