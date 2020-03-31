
# Beehive nodes API server
 
This API server exposes node information from the mysql database and other sources.


# usage

examples:
```bash
curl 'http://localhost:80/api/nodes/' | jq .

curl 'http://localhost:80/api/nodes/?filter=node_id,name,reverse_ssh_port,opmode,project,description,location&format=csv'

curl 'http://external-domain:80/api/nodes/?filter=node_id,rmq_connection,data_frames&format=csv'

curl 'http://localhost:8183/?filter=node_id,reverse_ssh_port,rssh_connection' | jq .
```

Note that the path `/api/nodes/` is required if you access the nodes-api via the beehive nginx. 


## fields

| field name              | type       | description                 |
| ----------------------- | ---------- | ----------------------------|
| **node_id**             | _string_   | unique identifier of node   |
| **project**             | _string_   |                             |
| **description**         | _string_   |                             |
| **reverse_ssh_port**    | _integer_  | the port reserved for reverse ssh tunnel |
| **hostname**            | _string_   |                             |
| **name**                | _string_   |                             |
| **location**            | _string_   |                             |
| **last_updated**        | _string_   |                             |
| **opmode**              | _string_   |                             |
| **groups**              | _string_   |                             |
| **iccid**               | _string_   |                             |
| **imei**                | _string_   |                             |
| **lon**                 | _float_    |                             |
| **lat**                 | _float_    |                             |
| non-mysql fields: |           |            
| **rssh_connection**     | _boolean_  | indicates if connection was established sometoime in the last 15 minutes |
| **rmq_connection**      | _boolean_  | indicates if node sent a rabbitmq message in the last 5 minutes |
| **data_frames**         | _integer_  | number of data frames in last 5 minutes |



## format

Default output format is json, but `format=csv` is also possible.



# Notes

optional docker flag:
```
-e FLASK_ENV=development
```