<!--
waggle_topic=Waggle/Beehive/Service
-->

# Nginx HTTP Server


This is the Beehive Nginx server.

## Build image:
```bash
docker rm -f beehive-nginx
docker rmi waggle/beehive-nginx
docker build -t waggle/beehive-nginx .
```


## Run
```bash
docker rm -f beehive-nginx
[ ! -z "$DATA" ] && \
docker run \
  -d \
  --name=beehive-nginx \
  --net beehive \
  -p 80:80 \
  waggle/beehive-nginx /usr/sbin/nginx -g 'daemon off;'
```
