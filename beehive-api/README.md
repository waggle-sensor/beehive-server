
# Beehive API server
 

This is the Beehive API server. 

## Build image:
```bash
docker rm -f beehive-api
docker rmi waggle/beehive-api
docker pull waggle/beehive-server
docker build -t waggle/beehive-api .
```


## Run
```bash
docker rm -f beehive-api
[ ! -z "$DATA" ] && \
docker run \
  -d \
  --name=beehive-api \
  --net beehive \
  -p 80:8183 \
  waggle/beehive-api
```
