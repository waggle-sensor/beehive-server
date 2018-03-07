# Publishing Tools

Tools to help publish approved project and sensor data.

## Metadata

The metadata for a project consists of a directory `project/` with the following items:

* `project/nodes.csv`: Table of node information.
* `project/events.csv`: Table of node events.

Each of these will be described below.

### Node Table

The node information table is a CSV file with the following fields:

1. Node ID
2. Project ID
3. VSN
4. Street Address
5. Latitude
6. Longitude
7. Description

For example, valid file contents would look like:

```
node_id,project_id,vsn,address,lat,lon,description
001e0610b9e5,AoT Chicago,02F,Sheridan Rd & Granville Ave,41.994454,-87.6553316,AoT Chicago (S) [C]
001e0610b9e9,AoT Chicago,080,Broadway Ave & Lawrence Ave,41.9691029,-87.6601463,AoT Chicago (S) [C]
001e0610ba16,AoT Chicago,010,Ohio St & Grand Ave,41.891897,-87.627507,AoT Chicago (S) [C]
001e0610ba18,AoT Chicago,01D,Damen Ave & Cermak,42.0024119,-87.6796016,AoT Chicago (S)
```

_The header is required!_

### Events Table

The node events table is a CSV file with the following fields:

1. Node ID
2. Timestamp
3. Event (Either `commissioned`, `decommissioned`, `retired`.)
4. Comment

For example, valid file contents would look like:

```
node_id,timestamp,event,comment
001e0610b9e5,2018/01/02 15:06:52,commissioned,
001e0610b9e9,2018/02/16 00:20:00,commissioned,
001e0610ba16,2018/02/19 22:14:35,commissioned,Deployed with experimental sensor.
001e0610ba16,2018/03/19 22:14:35,decommissioned,Took down to remove sensor.
001e0610ba16,2018/04/19 22:14:35,commissioned,Standard deployment.
001e0610ba16,2018/05/19 22:14:35,retired,Completed experiment.
001e0610ba18,2018/01/02 15:28:43,commissioned,
001e0610ba3b,2017/11/21 16:33:16,commissioned,
001e0610ba57,2018/01/02 15:04:46,commissioned,
```
