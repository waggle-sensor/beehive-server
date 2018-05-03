## Data manipulation utility

This tool is designed particularly to manipulate a large amount of data and provides a subset of the data that users are mostly interested in.

### Design diagram

The tool takes a csv that contains field headers and corresponding field data as input and manipulates it based on given operations. This process can be interative such that users can run this tool multiple times to get a narrower/smaller set of data of their interest.

```
 [Sensor data] --------> [ Manipulator ] --> [ Output sensor data ] ---> [ Manipulator ] --- << repeatable >>
   including        ^                                                ^
   nodes.csv        |                                                |
  sensors.csv   operations                                   another operations
```

### Commands

Supported commands are `grep`, `cut`, and `add`.

- `grep` is a command to filter data records
- `cut` is a command to remove fields
- `add` is a command to add fields

### How to use

*Note: the tool looks for `nodes.csv` and `sensors.csv` at the same directory that `data.csv` is located*

Synopsis:
```
$ python3 manipulator.py -h
usage: manipulator.py [-h] [-i INPUT] [-o OUTPUT] [-g GREP_OP] [-c CUT_OP]
                      [-a ADD_OP]

Manipulate csv dataset

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
  -o OUTPUT, --output OUTPUT
  -g GREP_OP, --grep GREP_OP
  -c CUT_OP, --cut CUT_OP
  -a ADD_OP, --add ADD_OP
```

Example 1: Get all records timestamped on a particular date
```
$ python3 manipulator.py -i dataset.csv -g 2018/04/29 -o output.csv
[ INFO  ] took 0.00 seconds for the manipulation
$ head -n 5 output.csv
timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf
2018/04/29 00:02:07,001e06107c9e,net,lan,rx,109803285,109803285
2018/04/29 00:02:07,001e06107c9e,net,lan,tx,102549843,102549843
2018/04/29 00:02:07,001e06107c9e,net,usb,rx,326011788,326011788
2018/04/29 00:02:07,001e06107c9e,net,usb,tx,287997173,287997173
```

Example 2: Get All records timestamped on a particular date and add `vsn`
```
$ python3 manipulator.py -i dataset.csv -g 2018/04/29 -o output.csv -a nodes.vsn
[ INFO  ] took 0.00 seconds for the manipulation
$ head -n 5 output.csv
timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf,vsn
2018/04/29 00:02:07,001e06107c9e,net,lan,rx,109803285,109803285,BRT
2018/04/29 00:02:07,001e06107c9e,net,lan,tx,102549843,102549843,BRT
2018/04/29 00:02:07,001e06107c9e,net,usb,rx,326011788,326011788,BRT
2018/04/29 00:02:07,001e06107c9e,net,usb,tx,287997173,287997173,BRT
```

Example 3: Do the same with __Example 2__ and additionally add `lat`, `lon` and remove `node_id`
```
$ python3 manipulator.py -i dataset.csv -g 2018/04/29 -o output.csv -a "nodes.vsn nodes.lat nodes.lon" -c node_id
[ INFO  ] took 0.00 seconds for the manipulation
$ head -n 5 output.csv
timestamp,subsystem,sensor,parameter,value_raw,value_hrf,vsn,lat,lon
2018/04/29 00:02:07,net,lan,rx,109803285,109803285,BRT,41.906481,-87.671373
2018/04/29 00:02:07,net,lan,tx,102549843,102549843,BRT,41.906481,-87.671373
2018/04/29 00:02:07,net,usb,rx,326011788,326011788,BRT,41.906481,-87.671373
2018/04/29 00:02:07,net,usb,tx,287997173,287997173,BRT,41.906481,-87.671373
```

Example 4: Get temperature sensor readings only, add `unit`, `lat`, `lon`, and remove `value_raw` and `node_id`
```
$ python3 manipulator.py -i dataset.csv -g temperature -o output.csv -a "sensors.unit nodes.lat nodes.lon" -c "value_raw node_id"
[ INFO  ] took 0.00 seconds for the manipulation
$ head output.csv
timestamp,subsystem,sensor,parameter,value_hrf,lat,lon,unit
2018/04/29 23:59:12,metsense,tsys01,temperature,25.46,41.906481,-87.671373,
2018/04/29 23:59:12,lightsense,hih6130,temperature,26.77,41.906481,-87.671373,
2018/04/29 23:59:12,lightsense,tmp421,temperature,22.69,41.906481,-87.671373,
2018/04/29 23:59:37,metsense,bmp180,temperature,29.0,41.906481,-87.671373,
2018/04/29 23:59:37,metsense,htu21d,temperature,24.14,41.906481,-87.671373,
2018/04/29 23:59:37,metsense,pr103j2,temperature,24.9,41.906481,-87.671373,
2018/04/29 23:59:37,metsense,tmp112,temperature,24.69,41.906481,-87.671373,
2018/04/29 23:59:37,metsense,tsys01,temperature,25.17,41.906481,-87.671373,
2018/04/29 23:59:37,lightsense,hih6130,temperature,26.71,41.906481,-87.671373,
2018/04/29 23:59:37,lightsense,tmp421,temperature,22.62,41.906481,-87.671373,
```
