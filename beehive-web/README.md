
# Beehive web/API server
 

This is a webserver and an API server. Those will be split into two scripts in the future.


## Build image:
```bash
docker rm -f beehive-web
docker rmi waggle/beehive-web
docker pull waggle/beehive-server
docker build -t waggle/beehive-web .
```


## Run
```bash
docker rm -f beehive-web
[ ! -z "$DATA" ] && \
docker run \
  -d \
  --name=beehive-web \
  --net beehive \
  -p 80:80 \
  waggle/beehive-web
```
