# Publishing Filter Tools and Metadata

## Overview

This document describes a set of tools which can be used to produce consumer
ready data from beehive.

They are intended to be used with different project + sensor metadata in order
to produce a personalized view of the data for each consumer. For example:

```
                                       +-> [Publishing Filter] -> [Data ready for MCS]
                                       |           ^
                                       |      MCS metadata (all nodes / all sensors)
                                       |
                                       |
[Converted / Calibrated Sensor Data] --+-> [Publishing Filter] -> [Data ready for Plenario]
                                       |          ^
                                       |    Plenario metadata (aot nodes / environmental sensors)
                                       |
                                       |
                                       +-> [...]
```

A complete publishing filter is composed of the following more specific tools:

* `filter-view`: Filters a sensor stream, only allowing data from a set of nodes during their commissioning dates.
```
                    project metadata
                          v
[Sensor Stream] -> [Filter View] -> [Sensor Stream]
                                           ^
                                  only data from nodes in view
                                   during commissioning date
```

* `filter-sensors`: Filters a sensor stream, only allowing "sane" sensors and values.
```
                     sensor metadata
                           v
 [Sensor Stream] -> [Filter Sensors] -> [Sensor Stream]
                                               ^
                                   only data from specified sensors
                                    with values in sanity range
```

Concretely, a sensor stream IO format is just a newline separated, CSV-like format of sensor
values:

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
```

_Output is in the same format, but can contain only a subset of the lines._

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

## Usage

A complete example is given at `examples/example-plenario.sh`. It uses the
`examples/plenario` project metadata, the `examples/climate.csv` sensor metadata
and sample data `examples/recent.csv`. We will reference this example, as we
walk through the details of building the following complete pipeline:

```
                  project metadata
                         v
[Sensor Stream] -> [Filter View] -> [Filter Sensors] -> [Sensor Stream]
                                          ^
                                    sensors metadata
```

First, we'll translate this into the shell script:

```sh
#!/bin/sh

# working directory is publishing-tools
cat examples/recent.csv |
bin/filter-view examples/plenario |
bin/filter-sensors examples/climate.csv >
filtered-sensor-data.csv
```

This will take the data in `recent.csv`, which includes sample data from many
different nodes and sensors:

```sh
$ cat examples/recent.csv | head
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;TSYS01;temperature;9.04
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;SPV1840LR5H-B;intensity;814
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;HIH4030;humidity;459
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;MLX75305;intensity;31162
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;BMP180;temperature;9.25
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;BMP180;pressure;100301
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;TSL250RD-LS;intensity;21952
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;TSL260RD;intensity;21092
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;MMA8452Q;acceleration.y;-1.0
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;MMA8452Q;rms;1.0

$ cat examples/recent.csv | wc -l
   67767
```

First, we apply `filter-view` which only keeps data from nodes in
`examples/plenario/nodes.csv` during a valid commissioning interval in
`examples/plenario/events.csv`:

```sh
$ cat examples/recent.csv | bin/filter-view examples/plenario | head
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;TSYS01;temperature;9.04
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;SPV1840LR5H-B;intensity;814
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;HIH4030;humidity;459
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;MLX75305;intensity;31162
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;BMP180;temperature;9.25
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;BMP180;pressure;100301
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;TSL250RD-LS;intensity;21952
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;TSL260RD;intensity;21092
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;MMA8452Q;acceleration.y;-1.0
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;MMA8452Q;rms;1.0

$ cat examples/recent.csv | bin/filter-view examples/plenario | wc -l
   19293
```

Second, we apply `filter-sensors` which only keeps data from sensors in
`examples/climate.csv`:

```sh
$ cat examples/recent.csv | bin/filter-view examples/plenario | bin/filter-sensors examples/climate.csv | head
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;TSYS01;temperature;9.04
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;BMP180;temperature;9.25
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;HTU21D;humidity;36.72
001e0610ef29;2018/02/26 16:48:48;coresense:3;frame;HTU21D;temperature;9.39
001e0610ef29;2018/02/26 16:49:14;coresense:3;frame;TSYS01;temperature;9.05
001e0610ef29;2018/02/26 16:49:14;coresense:3;frame;BMP180;temperature;9.3
001e0610ef29;2018/02/26 16:49:14;coresense:3;frame;HTU21D;humidity;37.08
001e0610ef29;2018/02/26 16:49:14;coresense:3;frame;HTU21D;temperature;9.41
001e0610ef29;2018/02/26 16:49:37;coresense:3;frame;TSYS01;temperature;9.04
001e0610ef29;2018/02/26 16:49:37;coresense:3;frame;BMP180;temperature;9.3

$ cat examples/recent.csv | bin/filter-view examples/plenario | bin/filter-sensors examples/climate.csv | wc -l
    2256
```

Finally, we write the result to `filtered-sensor-data.csv` which is ready for
further packaging or pushing to a consumer.
