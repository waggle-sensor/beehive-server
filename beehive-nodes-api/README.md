
# Beehive nodes API server
 
This API server exposes node information from the mysql database.


# usage

```bash
curl 'http://localhost:80/api/nodes/' | jq .

curl 'http://localhost:80/api/nodes/?filter=node_id,name,reverse_ssh_port,opmode,project,description,location,iccid,imei&format=csv'
```

## Reverse ssh tunnel

**reverse_ssh_port** inidicates the port reserved for reverse ssh tunnel

**rssh_connection** indicates if connection was established sometoime in the last 15 minutes

```bash
curl 'http://localhost:8183/?filter=node_id,reverse_ssh_port,rssh_connection' | jq .
```


## run image
docker run \
  -ti \
  --rm \
  --name=beehive-nodes-api \
  --net beehive \
  -p 8183:5000 \
  -e FLASK_ENV=development \
  -e MYSQL_HOST="beehive-mysql" \
  -e MYSQL_USER="waggle" \
  -e MYSQL_PASSWD="waggle" \
  -e MYSQL_DB="waggle" \
  waggle/beehive-nodes-api

-v `pwd`:/code 


## Notes

optional docker flag:
```
-e FLASK_ENV=development
```