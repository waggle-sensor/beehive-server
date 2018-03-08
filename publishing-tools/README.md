# Publishing Filter Tools and Metadata

This document describes a set of tools which can be used to produce consumer
ready data from beehive.

They are intended to be used with different project / sensor metadata in
order to generate a personalized view of the data for each consumer. For example:

```
                                       +-> [Publishing Filter] -> [Data ready for MCS]
                                       |           ^
                                       |      MCS Metadata
                                       |
[Converted / Calibrated Sensor Data] --+-> [Publishing Filter] -> [Data ready for Plenario]
                                       |          ^
                                       |    Plenario Metadata
                                       |
                                       +-> [...]
```

## Overview

The `filter-view` and `filter-sensors` tools input / output lines of sensor data with invalid values filtered out.

The `filter-view` tool only allows data from a set of nodes during valid
commissioning intervals.

```
                    project metadata
                          v
[Sensor Stream] -> [Filter View] -> [Sensor Stream]
                                           ^
                                  only data from nodes in view
                                   during commissioning date
```

The `filter-sensors` tool only allows data from a set of sensors passing a
sanity check.

```
                     sensor metadata
                           v
 [Sensor Stream] -> [Filter Sensors] -> [Sensor Stream]
                                               ^
                                   only data from specified sensors
                                    with values in sanity range
```

### Example

A concrete example is given here. Suppose we build a complete pipeline:

```
                  project metadata
                         v
[Sensor Stream] -> [Filter View] -> [Filter Sensors] -> [Sensor Stream]
                                          ^
                                    sensors metadata
```


Given the following sensor stream:

```
001e06109f62;2018/02/26 17:00:56;coresense:4;frame;HTU21D;temperature;29.78
001e06109f62;2018/02/26 17:00:56;coresense:4;frame;SPV1840LR5H-B;intensity;63.03
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;h2s;63
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;co;5238
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;so2;634
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;o3;5198
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;oxidizing_gases;22637
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;reducing_gases;6992
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;no2;1266
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;SHT25;humidity;42.55
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;SHT25;temperature;11.34
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;TSL260RD;intensity;49
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;MMA8452Q;acceleration.y;-0.99
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;MMA8452Q;rms;0.99
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;MMA8452Q;acceleration.x;-0.04
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;MMA8452Q;acceleration.z;-0.04
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;HIH6130;humidity;28.47
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;HIH6130;temperature;41.41
001e0610c2db;2018/02/26 16:53:30;coresense:3;frame;HIH6130;temperature;321.41
```

Suppose `filter-view` is configured to only allow `001e0610e537` and `001e0610c2db`.
Then, the output from `filter-view` will look like:

```
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;h2s;63
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;co;5238
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;so2;634
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;o3;5198
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;oxidizing_gases;22637
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;reducing_gases;6992
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;Chemsense;no2;1266
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;SHT25;humidity;42.55
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;SHT25;temperature;11.34
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;TSL260RD;intensity;49
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;MMA8452Q;acceleration.y;-0.99
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;MMA8452Q;rms;0.99
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;MMA8452Q;acceleration.x;-0.04
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;MMA8452Q;acceleration.z;-0.04
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;HIH6130;humidity;28.47
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;HIH6130;temperature;41.41
001e0610c2db;2018/02/26 16:53:30;coresense:3;frame;HIH6130;temperature;321.41
```

Suppose `filter-sensors` only allows reasonable temperature and humidity sensors.
Then, the output from `filter-sensors` may look like:

```
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;SHT25;humidity;42.55
001e0610e537;2018/02/26 17:02:24;coresense:4;frame;SHT25;temperature;11.34
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;HIH6130;humidity;28.47
001e0610c2db;2018/02/26 16:53:27;coresense:3;frame;HIH6130;temperature;41.41
```

In this case, we filtered out both nodes and specific sensors _and the data format
is the same throughout the pipeline_.

## Tools

The main building blocks are:

* `filter-view`: Filter commissioned data for a project.
* `filter-sensors`: Filter "sane" sensors and values.

These can be used to build publishing pipelines which take a stream of CSV format
lines and output only those satisfying... . For example:

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
