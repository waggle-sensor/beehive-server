# beehive-mysql navigation examples

## mysql client

```bash
source beehive.conf
docker exec -ti beehive-mysql mysql --database=${MYSQL_DB} --user=${MYSQL_USER} --password=${MYSQL_PASSWD}
or 
docker exec -ti beehive-mysql mysql --database=${MYSQL_DB} --user=root --password=${MYSQL_ROOT_PASSWORD}
```

or start client in new container for remote mysql:
```
source /opt/beehive/beehive-config/beehive.conf
docker run --env-file=/opt/beehive/beehive-config/beehive.conf  -ti --rm mysql:8 mysql --host=${MYSQL_HOST} --database=${MYSQL_DB} --user=${MYSQL_USER} --password=${MYSQL_PASSWD}
```


## view tables

```SQL
use waggle;
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM nodes;
```

## set description for a node

```SQL
UPDATE nodes SET description = "<description>" WHERE node_id="<node_id>";
```

## set description and a hostname for a node

```SQL
UPDATE nodes SET description = "<description>", hostname = "<hostname>" WHERE node_id="<node_id>";
```

## write hardware info

```SQL
UPDATE nodes SET hardware = '<JSON>' WHERE node_id="<node_id>";
```

## execute querys directly from the host:

```bash
docker exec -ti beehive-mysql mysql  -u waggle --password=waggle -e "use waggle; SELECT * FROM nodes;"
```

## delete entries:

```SQL
DELETE FROM nodes WHERE node_id = "0000000000AAAAAA";
```

## Admin Tasks

### Resetting Passwords

_Note: We may want to configure passwords to not expire!_

First, check the mysql version. There seems to be a lot of advice for resetting passwords and the following may only apply for our setup.

```bash
docker exec -ti beehive-mysql mysql --version
mysql  Ver 14.14 Distrib 5.7.10, for Linux (x86_64) using  EditLine wrapper
```

Now, connect using mysql client in container.

```bash
docker exec -ti beehive-mysql mysql --user=root --password=waggle
```

Finally, execute these reset commands.

```sql
SET PASSWORD FOR 'root' = PASSWORD('waggle');
SET PASSWORD FOR 'waggle' = PASSWORD('waggle');
```
