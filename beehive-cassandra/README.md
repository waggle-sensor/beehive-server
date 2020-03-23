


#### Notes


To directly connect to cassandra:
```bash
docker exec -ti beehive-cassandra cqlsh 
```


To view database (after it is created), e.g.:
```bash
DESCRIBE keyspaces;

use waggle;
DESCRIBE TABLES;
SELECT * FROM sensor_data_raw;
SELECT * FROM data_messages_v2;
```

