
# Beehive rehistration
 
This API server accepts registration requests from waggle nodes.


## build image:
```bash
docker rm -f beehive-registration
docker rmi waggle/beehive-registration
docker build -t waggle/beehive-registration .
```



## run image
docker run \
  -ti \
  --rm \
  --name=beehive-registration \
  --net beehive \
  -p 8183:5000 \
  -e FLASK_ENV=development \
  -e MYSQL_HOST="beehive-mysql" \
  -e MYSQL_USER="waggle" \
  -e MYSQL_PASSWD="waggle" \
  -e MYSQL_DB="waggle" \
  waggle/beehive-registration

-v `pwd`:/code 


## Notes

optional docker flag:
```
-e FLASK_ENV=development
```