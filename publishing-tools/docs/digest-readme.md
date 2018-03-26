# Data Digest

## Overview

This digest contains the following data files:

* `data.csv` - Sensor data.
* `metadata/nodes.csv` - Node metadata.
* `metadata/sensors.csv` - Sensor metadata.

These files are described in-depth in the following sections.

### Sensor Data

The sensor data file is an aggregate of all _published_ data from a project's
nodes. By published, we mean:

* Data was read from a whitelisted node belonging to the project.
* Data was read during that node's commissioning time.
* Data was read from a whitelisted sensor.
* Data value passed a simple range check. (Range is specified in sensor metadata.)

This file is a CSV with the following fields:

* `node_id` - ID of node which produced the reading.
* `timestamp` - UTC timestamp when reading was produced.
* `plugin` - Plugin which produced reading.
* `sensor` - Sensor which produced reading.
* `parameter` - Specific parameter from sensor.
* `value` - Reading value.

For example:
```
node_id,timestamp,plugin,sensor,parameter,value
001e0610b9e5,2017/11/28 17:20:58,coresense:3,BMP180,temperature,14.1
001e0610b9e5,2017/11/28 17:20:58,coresense:3,TSYS01,temperature,14.48
001e0610b9e5,2017/11/28 17:20:58,coresense:3,HTU21D,temperature,14.87
001e0610b9e5,2017/11/28 17:20:58,coresense:3,HTU21D,humidity,36.51
001e0610b9e5,2017/11/28 17:21:22,coresense:3,TSYS01,temperature,14.56
```

More information about nodes and sensors is discussed in the next two sections.


*Note: Currently, we _do not_ do automatic in-depth or cross sensor comparison and
filtering. For example, a damaged sensor _could_ repeat an error value over and over if
in the accepted range or a node _could_ have a sensor deviate from its neighbors.*

### Node Metadata

The node metadata provides additional information about each of a project's nodes. This
file is a CSV with the following fields:

* `node_id` - ID of node.
* `project_id` - ID of project which manages node.
* `vsn` - Public name for node. The VSN is visible on the physical enclosure.
* `address` - Street address of node.
* `lat` - Latitude of node.
* `lon` - Longitude of node.
* `description` - More detailed description of node's build and configuration.

For example:
```
node_id,project_id,vsn,address,lat,lon,description
001e0610bc10,AoT Chicago,01F," State St & 87th Chicago IL",41.736314,-87.624179,AoT Chicago (S) [C]
001e0610ba8b,AoT Chicago,018," Stony Island Ave & 63rd St Chicago IL",41.7806,-87.586456,AoT Chicago (S) [C]
001e0610ba18,AoT Chicago,01D," Damen Ave & Cermak Chicago IL",41.852179,-87.675825,AoT Chicago (S)
001e0610ba81,AoT Chicago,040," Lake Shore Drive & 85th St Chicago IL",41.741148,-87.54045,AoT Chicago (S)
001e0610ba16,AoT Chicago,010," Ohio St & Grand Ave Chicago IL",41.891964,-87.611603,AoT Chicago (S) [C]
```

### Sensor Metadata

The sensor metadata provides additional information about each of the sensors published
by the project. This file is a CSV with the following fields:

* `sensor` - Sensor name.
* `parameter` - Sensor parameter.
* `unit` - Physical units of sensor value.
* `minval` - Minimum value according to datasheet.
* `maxval` - Maximum value according to datasheet.
* `datasheet` - Reference to sensor's datasheet.

For example:
```
sensor,parameter,unit,minval,maxval,datasheet
HTU21D,humidity,RH,0,100,"https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf"
HTU21D,temperature,C,-40,125,"https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf"
BMP180,temperature,C,-40,85,"https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf"
BMP180,pressure,hPa,300,1100,"https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf"
TSYS01,temperature,C,-40,125,"https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/tsys01.pdf"
```

More in-depth information can be found at: https://github.com/waggle-sensor/sensors
