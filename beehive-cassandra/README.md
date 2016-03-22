### Cassandra

Be sure that environment variable $DATA is defined.
```bash
[ ! -z "$DATA" ] && \
docker run -d \
--name beehive-cassandra \
--net beehive \
-v ${DATA}/cassandra/:/var/lib/cassandra/ \
--ulimit memlock=unlimited \
--ulimit nofile 100000 \
--ulimit nproc 32768 \
cassandra:3.2 -R
```
For simple testing without much data you can omit option "-v" above. Without "-v" Cassandra data is not stored persistently and data is lost when the container is removed. Add port mapping "-p 7000:7000" if the beehive server does not run on the same host as the cassandra database.


Installation instructions for Cassandra without Docker:

http://docs.datastax.com/en/cassandra/2.0/cassandra/install/installDeb_t.html


#### Notes

To directly connect to cassandra:
```bash
docker run -it --link beehive-cassandra:cassandra --rm cassandra:3.2 cqlsh cassandra
```
To view database, e.g.:
```bash
use waggle;
DESCRIBE TABLES;
SELECT * FROM nodes;
SELECT * FROM sensor_data;
```
