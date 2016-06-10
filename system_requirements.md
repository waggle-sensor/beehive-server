
#System requirement for beehive1.mcs.anl.gov


## beehive1

4 CPUs
16GB RAM (can be less without cassandra)
40 GB disk space


Ports
80 : web (world-wide)
22 : ssh (ANL only)
8183 : API (world-wide)
23181 : RabbitMQ (world-wide)
24181 : certificate server (ANL only)



## cassandra cluster
(3 instances each)

16 GB RAM
40 GB disk space


Ports:

80 : web (ANL only)
22 : ssh (ANL only)

23181 : RabbitMQ (for testing)
23182 : RabbitMQ (for cluster communication testing)

7000 : cassandra cluster communication
7001 : cassandra cluster communication using ssl




