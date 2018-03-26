# Data Digest

## Overview

This digest should contain the following data files:

* `data.csv`
* `metadata/nodes.csv`
* `metadata/sensors.csv`

These files are described in-depth in the following sections.

### Sensor Data - `data.csv`

`data.csv` is an aggregate of all _published_ data from a project's nodes.
By published, we mean:

* Data was read from whitelisted node.
* Data was read during node's commissioning time.
* Data was read from whitelisted sensor.
* Data passes simple range check.

*Note: We do not do automatic, detailed sensor filtering. For example, a damaged sensor _could_ produce values in an accepted range, but repeat the same default value over and over.*

`data.csv` follows a CSV format with the following fields:

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
001e0610b9e5,2017/11/28 17:21:22,coresense:3,HTU21D,temperature,14.92
```

More information about nodes and sensors is discussed in the next two sections.

### Node Metadata - `metadata/nodes.csv`

### Sensor Metadata - `metadata/sensors.csv`

More in-depth information can be found at: https://github.com/waggle-sensor/sensors
