
# Certificate Server for Waggle
 
Do not use this for production purposes ! 

## web.py
The required python package web.py is already included in the depedencies of the beehive server. If web.py is not already installed it can be installed in one of these ways:
```bash
apt-get install python-webpy
#or
pip install web.py
```

## Run
```bash
docker rm -f beehive-cert
docker run -ti \
  -p 24181:80 \
  -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
  --name beehive-cert \
  waggle/beehive-server /bin/bash
cd /usr/lib/waggle/beehive-server/cert-serve ; ./cert-serve.py
```
