
# Beehive Flask server
 

This is the Beehive Flask server. 

## OS Dependencies

```bash
libmysqlclient-dev (11MB)
python3-dev (55MB)
```

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
  -p 8183:80 \
  waggle/beehive-api
```
