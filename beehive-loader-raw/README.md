<!--
waggle_topic=Waggle/Beehive/Services
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
