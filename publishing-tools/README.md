# Publishing Tools and Metadata

This document describes a set of tools which produce consumer ready sensor data from beehive.

## Tools

The main building blocks are:

* `filter-view`: Filter commissioned data for a project.
* `filter-sensors`: Filter "sane" sensors and values.

These can be used to build publishing pipelines. For example:

```sh
cat sensor-data.csv |
filter-view project-metadata |
filter-sensors sensor-metadata.csv >
filtered-sensor-data.csv
```

## Metadata

Each tool requires an argument specifying which metadata file it should use.

### Project Metadata

Project metadata consists of a directory `project/` with the following items:

* `project/nodes.csv`: Table of node information.
* `project/events.csv`: Table of node events.

Each of these will be described below.

#### Node Table

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

#### Events Table

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

_The header is required!_

### Sensor Metadata

Sensor metadata is a CSV file with the following fields:

1. Sensor ID
2. Min Value
3. Max Value

For example, valid file contents would look like:

```
sensor_id,minval,maxval
HTU21D.humidity,-1,101
HTU21D.temperature,-40,50
BMP180.temperature,-40,50
BMP180.pressure,300,1100
TSYS01.temperature,-40,50
```

_The header is required!_
