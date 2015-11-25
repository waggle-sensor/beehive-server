### Cassandra

Be sure that environment variable $DATA is defined.
```bash
docker run -d \
--name beehive-cassandra \
-v ${DATA}/cassandra/data/:/var/lib/cassandra/data \
-p 7000:7000 \
cassandra:2.2.3
```
For simple testing without much data you can omit option "-v" above. Without "-v" Cassandra data is not stored persistently and data is lost when the container is removed. The port mapping "-p 7000:7000" can be omitted if the beehive server runs on the same host as the cassandra database.

Create tables:
```bash
export WCS=$(curl https://raw.githubusercontent.com/waggle-sensor/beehive-server/master/waggle_cassandra_setup.cql)
echo ${WCS}
docker exec -ti beehive-cassandra cqlsh.py -e "${WCS}"
```


Installation instructions for Cassandra without Docker:

http://docs.datastax.com/en/cassandra/2.0/cassandra/install/installDeb_t.html


#### Notes

To directly connect to cassandra:
```bash
docker run -it --link beehive-cassandra:cassandra --rm cassandra:2.2.3 cqlsh cassandra
```
To view database, e.g.:
```bash
use waggle;
DESCRIBE TABLES;
SELECT * FROM node_info;
SELECT * FROM sensor_data;
```
