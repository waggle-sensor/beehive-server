<!--
waggle_topic=/beehive/services
-->

# Raw Data Loader

This tool is a simple, reliable ETL process which moves raw data from the
RabbitMQ incoming data queue into Cassandra.

```
                                                     +-----------------+
                                                     |                 |
                                                     |    Cassandra    |
+---------------------+                              |                 |
| Incoming Data Queue | ---> beehive-loader-raw ---> | sensor_data_raw |
+---------------------+             ^                |                 |
                              1. Get message         |                 |
                              2. Get metadata        +-----------------+
                              3. Insert to DB
                              4. ACK message
```

## Deployment

beehive-loader-raw is packaged as a Docker image. It can be built and deployed
as follows:

```
cd beehive-server/beehive-loader-raw
make build
make deploy
```
