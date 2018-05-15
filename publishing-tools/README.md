<!--
waggle_topic=Waggle/Beehive/Operations,Publishing Data
waggle_topic=Waggle/Data,Publishing Data
-->

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

The expected sensor stream format is just a semicolon delimited, CSV-like format with fields:

* UTC Timestamp
* Node ID
* Subsystem
* Sensor
* Parameter
* Value (Raw)
* Value (HRF)

For example:

```
timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf
2018/03/12 15:49:04,001e06113100,metsense,bmp180,pressure,11417504,1062.55
2018/03/12 15:49:04,001e06113100,metsense,bmp180,temperature,22717,14.5
2018/03/12 15:49:04,001e06113100,metsense,hih4030,humidity,537,81.4
2018/03/12 15:49:04,001e06113100,metsense,htu21d,humidity,34042,58.93
2018/03/12 15:49:04,001e06113100,metsense,htu21d,temperature,18968,4.01
2018/03/12 15:49:04,001e06113100,metsense,mma8452q,acceleration_x,65280,-15.625
2018/03/12 15:49:04,001e06113100,metsense,mma8452q,acceleration_y,49120,-1001.953
2018/03/12 15:49:04,001e06113100,metsense,mma8452q,acceleration_z,320,19.531
2018/03/12 15:49:04,001e06113100,metsense,pr103j2,temperature,659,4.55
```

_Input and output are in the same format, but output will usually contain a subset of the input._

## Metadata

Each tool accepts metadata to determine what values it will filter.

### Project Metadata

Project metadata consists of a directory `project/` with the following items:

* `project/nodes.csv`: Table of node information.
* `project/events.csv`: Table of node events.

Each of these will be described below.

#### Node Table

The node information table is a CSV file with the following fields:

* Node ID
* Project ID
* VSN
* Street Address
* Latitude
* Longitude
* Description

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

* Node ID
* Timestamp
* Event (Either `commissioned`, `decommissioned`, `retired`.)
* Comment

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

* Subsystem
* Sensor
* Parameter
* Unit
* Min Value
* Max Value
* Datasheet URL

For example, valid file contents would look like:

```
subsystem,sensor,parameter,unit,minval,maxval,datasheet
... update example ...
```

_The header is required!_

## Utilities

In addition to the main pipeline tools, the following utilities are included for
debugging or more efficiently interfacing with other components:

* `compile-digests`: Takes datasets tree of the form `node/date.csv.gz`, digest
build directory and a list of projects and compiles a complete project digest.
See program help for more information.

* `published-dates`: Takes project metadata and prints all commissioned nodes /
dates pairs up to and including today. May be useful for debugging or efficiently
selecting datasets for a digest.
