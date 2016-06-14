
Create certificate authority

```bash
docker pull waggle/beehive-server:latest

[ ! -z "$DATA" ] && docker run -ti \
  --name certs \
  --rm \
  -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
  waggle/beehive-server:latest ./SSL/create_certificate_authority.sh
```  
