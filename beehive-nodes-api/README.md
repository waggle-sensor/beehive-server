
# Beehive nodes API server
 
This API server exposes node information from the mysql database.


## build image:
```bash
docker rm -f beehive-nodes-api
docker rmi waggle/beehive-nodes-api
docker build -t waggle/beehive-nodes-api .
```



## run image
docker run \
  -ti \
  --rm \
  --name=beehive-nodes-api \
  --net beehive \
  -p 8183:5000 \
  -e FLASK_ENV=development \
  -e MYSQL_HOST="beehive-mysql" \
  -e MYSQL_USER="waggle" \
  -e MYSQL_PASSWD="waggle" \
  -e MYSQL_DB="waggle" \
  waggle/beehive-nodes-api

-v `pwd`:/code 


## Notes

optional docker flag:
```
-e FLASK_ENV=development
```