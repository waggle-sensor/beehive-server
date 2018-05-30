# Project Digest Readme

{%- if header %}

{{ header }}

{%- endif %}

The files in this directory contain sensor data and the associated meta-data that
will enable parsing the sensor values.

## Overview

This sensor data digest contains the following files:

* `data.csv.gz` - Sensor data ordered by ascending timestamp.
* `nodes.csv` - Nodes metadata.
* `sensors.csv` - Sensor metadata.
* `provenance.csv` - Provenance metadata.

These files will be described in-depth in the following sections.

### Sensor Data

The sensor data file is an aggregate of all published data from the project's
nodes. By published, we mean:

{%- if complete %}

* Data was read from a whitelisted node belonging to the project.
* Data was read during that node's commissioning period.
{% else %}

* Data was read from a whitelisted node belonging to the project.
* Data was read during that node's commissioning period.
* Data was read from a whitelisted sensor.
* Data value passed a simple range check - the value for the parameter is reasonable and within the possible values the sensor can generate. No further checks were made on the data.
{%- endif %}

The `data.csv.gz` file is a compressed CSV with the following, but not limited to, columns:

* `timestamp` - UTC timestamp of when the measurement was done.
* `node_id` - ID of node which did the measurement.
* `subsystem` - Subsystem of node containing sensor.
* `sensor` - Sensor that was measured.
* `parameter` - Sensor parameter that was measured.
* `value_raw` - Raw measurement value from sensor.
* `value_hrf` - Converted, "human readable" value from sensor.

These fields will always be provided as a header, for example:
```
timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf
2017/09/09 22:12:44,001e0610ba8f,lightsense,hih4030,humidity,NA,32.18
2017/09/09 22:12:44,001e0610ba8f,lightsense,hih4030,temperature,NA,48.55
2017/09/09 22:12:44,001e0610ba8f,lightsense,ml8511,intensity,9643,NA
2017/09/09 22:12:44,001e0610ba8f,lightsense,tmp421,temperature,NA,43.81
2017/09/09 22:12:44,001e0610ba8f,metsense,hih4030,humidity,450,NA
2017/09/09 22:12:44,001e0610ba8f,metsense,htu21d,humidity,NA,41.15
2017/09/09 22:12:44,001e0610ba8f,metsense,htu21d,temperature,NA,24.1
2017/09/09 22:12:44,001e0610ba8f,metsense,metsense,id,00001814B7E8,00001814B7E8
2017/09/09 22:12:44,001e0610ba8f,metsense,pr103j2,temperature,839,NA
```

Sensor data is ordered by ascending timestamp.

Additional information such each node's coordinates or each sensor units can be found
in the metadata. More information about these will be provided in the next two sections.

A sensor values may be marked `NA`, indicating that either the raw or HRF value is
unavailable.

{%- if not complete %}

*Note: Currently, we _do not_ do automatic in-depth or cross sensor comparison and
filtering. For example, a damaged sensor _could_ repeat an error value over and over if it is
in the accepted range or a node _could_ have a sensor value deviate from its neighbors.*
{%- endif %}

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

These fields will always be provided as a header, for example:
```
node_id,project_id,vsn,address,lat,lon,description
001e0610bc10,AoT Chicago,01F,"State St & 87th Chicago IL",41.736314,-87.624179,AoT Chicago (S) [C]
001e0610ba8b,AoT Chicago,018,"Stony Island Ave & 63rd St Chicago IL",41.7806,-87.586456,AoT Chicago (S) [C]
001e0610ba18,AoT Chicago,01D,"Damen Ave & Cermak Chicago IL",41.852179,-87.675825,AoT Chicago (S)
001e0610ba81,AoT Chicago,040,"Lake Shore Drive & 85th St Chicago IL",41.741148,-87.54045,AoT Chicago (S)
001e0610ba16,AoT Chicago,010,"Ohio St & Grand Ave Chicago IL",41.891964,-87.611603,AoT Chicago (S) [C]
```

Additional details about a node are contained in the description field. The letters
inside the brackets `[ ]` indicate:

* `C` - Node is equipped with chemical sensors.
* `A` - Node is equipped with Alphasense OPN-N2 air quality sensor.
* `P` - Node is equipped with Plantower PMS7003 air quality sensor.

### Sensor Metadata

The sensor metadata provides additional information about each of the sensors published
by the project. This file is a CSV with the following fields:

* `ontology` - Ontology of measurement.
* `subsystem` - Subsystem containing sensor.
* `sensor` - Sensor name.
* `parameter` - Sensor parameter.
* `hrf_unit` - Physical units of HRF value.
* `hrf_minval` - Minimum HRF value according to datasheet. Used as lower bound in range filter.
* `hrf_maxval` - Maximum HRF value according to datasheet. Used as upper bound in range filter.
* `datasheet` - Reference to sensor's datasheet.

These fields will always be provided as a header, for example:
```
ontology,subsystem,sensor,parameter,hrf_unit,hrf_minval,hrf_maxval,datasheet
/sensing/meteorology/pressure,metsense,bmp180,pressure,hPa,300,1100,"https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf"
/sensing/meteorology/temperature,metsense,bmp180,temperature,C,-40,125,"https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/bmp180.pdf"
/sensing/meteorology/humidity,metsense,hih4030,humidity,RH,0,100,"https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu4030.pdf"
/sensing/meteorology/humidity,metsense,htu21d,humidity,RH,0,100,"https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf"
/sensing/meteorology/temperature,metsense,htu21d,temperature,C,-40,125,"https://github.com/waggle-sensor/sensors/blob/master/sensors/airsense/htu21d.pdf"
```

More in-depth information about each sensor can be found at: https://github.com/waggle-sensor/sensors

### Provenance Metadata

The provenance metadata provides additional information about the origin of this
project digest. This file is a CSV with the following fields:

* `data_format_version` - Data format version.
* `project_id` - Project ID.
* `data_start_date` - Minimum possible publishing UTC timestamp.
* `data_end_date` - Maximum possible publishing UTC timestamp. If no explicit date exists, the creation date is used.
* `creation_date` - UTC timestamp this digest was created.
* `url` - URL where this digest was provided.

These fields will always be provide as a header, for example:
```
data_format_version,project_id,data_start_date,data_end_date,creation_date,url
1,AoT_Chicago.complete,2017/03/31 00:00:00,2018/04/10 15:34:36,2018/04/10 15:34:36,http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/AoT_Chicago.complete.latest.tar.gz
```

### Useful Links

* Sensors: https://github.com/waggle-sensor/sensors/blob/develop/README.md
* Array of Things: https://arrayofthings.github.io/
* Waggle: http://wa8.gl/

## Disclaimer

Although our goal is to provide stable metadata files, please consider these as
in-development. If you do write tools which process them, we *strongly* recommend
taking advantage of the metadata headers and processing the files as CSV when applicable in
order to accommodate future changes.
