

# Beehive MySQL


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

## MySQL examples

Please do not forget to change your password do something other than "waggle"

```bash
# enter the container
docker exec -ti beehive-mysql /bin/bash

# run the mysql client
mysql  -u root --password=waggle
mysql  -u waggle --password=waggle

# or run client directly
docker exec -ti beehive-mysql mysql  -u waggle --password=waggle

# view tables
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM nodes;


# execute querys directly from the host:
docker exec -ti beehive-mysql mysql  -u waggle --password=waggle -e "SELECT * FROM nodes;"

```

