
# Beehive nodes API server
 
This API server exposes node information from the mysql database.


# usage

```bash
curl 'http://localhost:80/api/nodes/' | jq .

curl 'http://localhost:80/api/nodes/?filter=node_id,name,reverse_ssh_port,opmode,project,description,location,iccid,imei&format=csv'
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