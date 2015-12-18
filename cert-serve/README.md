
```bash
docker run -ti -p 9999:9999 -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ --name cert-serve waggle/beehive-server /bin/bash
cd /usr/lib/waggle/beehive-server/cert-serve ; ./cert-serve.py
apt-get install python-webpy
pip install web.py
echo "unique_subject = no" > SSL/waggleca/index.txt.attr
```
