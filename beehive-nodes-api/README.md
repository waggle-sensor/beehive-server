
# Beehive nodes API server
 
This API server exposes node information from the mysql database.


# usage

examples:
```bash
curl 'http://localhost:80/api/nodes/' | jq .

curl 'http://localhost:80/api/nodes/?filter=node_id,name,reverse_ssh_port,opmode,project,description,location&format=csv'

curl 'http://beehive1.mcs.anl.gov:80/api/nodes/?filter=node_id,rmq_connection,data_frames&format=csv'

curl 'http://localhost:8183/?filter=node_id,reverse_ssh_port,rssh_connection' | jq .
```

## fields

| field name              | type       | description                 |
| ----------------------- | ---------- | ----------------------------|
| **node_id**             | _string_   | unique identifier of node   |
| **name**                | _string_   |                             |
| **opmode**              | _string_   |                             |
| **project**             | _string_   |                             |
| **description**         | _string_   |                             |
| **location**            | _string_   |                             |
| **reverse_ssh_port**    | _integer_  | the port reserved for reverse ssh tunnel |
| **rssh_connection**     | _boolean_  | indicates if connection was established sometoime in the last 15 minutes |
| **rmq_connection**      | _boolean_  | indicates if node sent a rabbitmq message in the last 5 minutes |
| **data_frames**         | _integer_  | number of data frames in last 5 minutes |



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