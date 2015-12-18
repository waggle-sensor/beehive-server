
# Certificate Server for Waggle
 
Do not use this for production purposes ! 


configuration:
```bash
apt-get install python-webpy
pip install web.py
```

Run:
```bash
docker rm -f cert-serve
docker run -ti -p 9999:9999 -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ --name cert-serve waggle/beehive-server /bin/bash
cd /usr/lib/waggle/beehive-server/cert-serve ; ./cert-serve.py
```
