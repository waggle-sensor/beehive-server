# beehive-mysql navigation examples


## mysql client
```bash
docker exec -ti beehive-mysql mysql  -u waggle --password=waggle
```

## view tables
```SQL
use waggle;
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM nodes;
```

## set description for a node
```SQL
UPDATE nodes SET description = "<description>" WHERE node_id="<node_id>";
```
## set description and a hostname for a node
```SQL
UPDATE nodes SET description = "<description>", hostname = "<hostname>" WHERE node_id="<node_id>";
```
## write hardware info
```SQL
UPDATE nodes SET hardware = '<JSON>' WHERE node_id="<node_id>";
```
## execute querys directly from the host:
```bash
docker exec -ti beehive-mysql mysql  -u waggle --password=waggle -e "use waggle; SELECT * FROM nodes;"
```
## delete entries:
```SQL
DELETE FROM nodes WHERE node_id = "0000000000AAAAAA";
```
