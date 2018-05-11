<!--
waggle_topic=Waggle/Beehive/Service
-->

# MySQL Database

## Start container:

```bash
docker rm -f beehive-mysql

[ ! -z "$DATA" ] && \
docker run -d \
  --name beehive-mysql \
  --net beehive \
  -v ${DATA}/mysql/datadir:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=waggle \
  -e MYSQL_DATABASE=waggle \
  -e MYSQL_USER=waggle \
  -e MYSQL_PASSWORD=waggle \
  mysql:5.7.10
```

## Create tables

```bash
curl https://raw.githubusercontent.com/waggle-sensor/beehive-server/master/beehive-mysql/tables.sql | docker exec -i beehive-mysql mysql  -u waggle --password=waggle
```

## MySQL examples

Please do not forget to change your password do something other than "waggle"

```bash
# run the mysql client
docker exec -ti beehive-mysql mysql  -u waggle --password=waggle

# view tables
use waggle;
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM nodes;

# set description for a node
UPDATE nodes SET description = "<description>" WHERE node_id="<node_id>";
# set description and a hostname for a node
UPDATE nodes SET description = "<description>", hostname = "<hostname>" WHERE node_id="<node_id>";
# write hardware info
UPDATE nodes SET hardware = '<JSON>' WHERE node_id="<node_id>";


# or execute querys directly from the host:
docker exec -ti beehive-mysql mysql  -u waggle --password=waggle -e "use waggle; SELECT * FROM nodes;"


#delete entries:
DELETE FROM nodes WHERE node_id = "0000000000AAAAAA";

```
## Drop tables (WARNING: DO NOT do this as part of installation)
Only do this while debugging - for example, to drop all the tables before testing their creation.

Note: The beehive server will not function properly without these tables - therefore, tables should be created after being DROPped.

```bash
curl https://raw.githubusercontent.com/waggle-sensor/beehive-server/master/beehive-mysql/dropTables.sql | docker exec -i beehive-mysql mysql  -u waggle --password=waggle
```
