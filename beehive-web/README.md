
# Beehive web/API server
 

This is a webserver and an API server. Those will be split into two scripts in the future.


## Run
```bash
docker pull waggle/beehive-server
docker rm -f beehive-web
[ ! -z "$DATA" ] && \
docker run -it \
  -d \
  --name=beehive-web \
  --net beehive \
  -p 80:80 \
  waggle/beehive-server \
  /usr/lib/waggle/beehive-server/beehive-web/webserver.py
```
