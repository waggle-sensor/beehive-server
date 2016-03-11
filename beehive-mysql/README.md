

# Beehive MySQL


Start container:

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


