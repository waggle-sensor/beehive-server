<!--
waggle_topic=/data_analysis/datatools,"Waggle CSV Data Manipulation Tool"
-->

# wg_datatool: Waggle CSV Data Manipulation Tool

All systems which build on the Waggle Platform share a common archive format for exported data.  This python tool helps manipulate the large comma-separated format (CSV) data from sensors: `data.csv`

## Design diagram

The program takes a CSV that contains field headers and corresponding rows of data and manipulates it based on command-line options. The tool can be applied repeatedly to extract data or build larger data products.

```
 [data.csv] ---> [wg_datatool] ---> [Output File1] ---> [wg_datatool] --- [Output File2] ---> ...
```

## Commands

Supported commands are `grep`, `cut`, and `add`.

- `grep` selects rows from the input file, such as by `timestamp` and/or `node_id`
- `cut` removes a column of data
- `add` adds a new column of data

## How to use

*Note: the tool looks for `nodes.csv` and `sensors.csv` at the same directory that `data.csv` is located*

Synopsis:
```
$ python3 wg_datatool.py --help
usage: wg_datatool.py [-h] [-v] [-i INPUT] [-o OUTPUT] [-g GREP_OP]
                      [-c CUT_OP] [-a ADD_OP] [-j CPU] [--all_cpu]

Manipulate csv dataset

optional arguments:
  -h, --help            show this help message and exit
  -v, --version
  -i INPUT, --input INPUT
                        Input file path
  -o OUTPUT, --output OUTPUT
                        Output file path
  -g GREP_OP, --grep GREP_OP
                        Grep operations
  -c CUT_OP, --cut CUT_OP
                        Cut operations
  -a ADD_OP, --add ADD_OP
                        Add operations
  -j CPU, --cpu CPU     Number of CPUs to use
  --all_cpu
```

Example 1: Get all records timestamped on a particular date
```
$ python3 wg_datatool.py -i dataset.csv -g 2018/04/29 -o output.csv --all_cpu
[ INFO  ] Took 0.00 seconds for input file indexing
[ INFO  ] Took 0.01 seconds for the manipulation
[ INFO  ] Took 0.00 seconds for merging output
[ INFO  ] Manipulation is completed.
$ head -n 5 output.csv
timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf
2018/04/29 00:02:07,001e06107c9e,net,lan,rx,109803285,109803285
2018/04/29 00:02:07,001e06107c9e,net,lan,tx,102549843,102549843
2018/04/29 00:02:07,001e06107c9e,net,usb,rx,326011788,326011788
2018/04/29 00:02:07,001e06107c9e,net,usb,tx,287997173,287997173
```

Example 2: Get `uptime` and `loadavg` at the time `23:54:54` on `2018/04/29`
```
$ python3 wg_datatool.py -i medium.csv -g "2018/04/29 and 23:54:54 and uptime or 2018/04/29 and 23:54:54 and loadavg" --all_cpu
[WARNING] Output file is not specified.
[ INFO  ] Output will be output.csv
[ INFO  ] Took 0.37 seconds for input file indexing
[ INFO  ] Took 0.56 seconds for the manipulation
[ INFO  ] Took 0.00 seconds for merging output
[ INFO  ] Manipulation is completed.
$ cat output.csv
timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf
2018/04/29 23:54:54,001e06107c9e,nc,uptime,uptime,889172,889172
2018/04/29 23:54:54,001e06107c9e,nc,uptime,idletime,3353470,3353470
2018/04/29 23:54:54,001e06107c9e,nc,loadavg,load_1,0.33,0.33
2018/04/29 23:54:54,001e06107c9e,nc,loadavg,load_5,0.37,0.37
2018/04/29 23:54:54,001e06107c9e,nc,loadavg,load_10,0.35,0.35
2018/04/29 23:54:54,001e06107c9e,ep,uptime,uptime,265854,265854
2018/04/29 23:54:54,001e06107c9e,ep,uptime,idletime,1226464,1226464
2018/04/29 23:54:54,001e06107c9e,ep,loadavg,load_1,0.13,0.13
2018/04/29 23:54:54,001e06107c9e,ep,loadavg,load_5,0.06,0.06
2018/04/29 23:54:54,001e06107c9e,ep,loadavg,load_10,0.07,0.07
2018/04/29 23:54:54,001e06107c9e,wagman,uptime,uptime,889823,889823
```

Example 3: Get All records timestamped on a particular date and add `vsn`
```
$ python3 wg_datatool.py -i dataset.csv -g 2018/04/29 -o output.csv -a nodes.vsn --all_cpu
[ INFO  ] Took 0.00 seconds for input file indexing
[ INFO  ] Took 0.01 seconds for the manipulation
[ INFO  ] Took 0.00 seconds for merging output
[ INFO  ] Manipulation is completed.
$ head -n 5 output.csv
timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf,vsn
2018/04/29 00:02:07,001e06107c9e,net,lan,rx,109803285,109803285,BRT
2018/04/29 00:02:07,001e06107c9e,net,lan,tx,102549843,102549843,BRT
2018/04/29 00:02:07,001e06107c9e,net,usb,rx,326011788,326011788,BRT
2018/04/29 00:02:07,001e06107c9e,net,usb,tx,287997173,287997173,BRT
```

Example 4: Do the same with __Example 2__ and additionally add `lat`, `lon` and remove `node_id`
```
$ python3 wg_datatool.py -i dataset.csv -g 2018/04/29 -o output.csv -a "nodes.vsn nodes.lat nodes.lon" -c node_id --all_cpu
[ INFO  ] Took 0.00 seconds for input file indexing
[ INFO  ] Took 0.01 seconds for the manipulation
[ INFO  ] Took 0.00 seconds for merging output
[ INFO  ] Manipulation is completed.
$ $ head -n 5 output.csv
timestamp,subsystem,sensor,parameter,value_raw,value_hrf,vsn,lat,lon
2018/04/29 00:02:07,net,lan,rx,109803285,109803285,BRT,41.906481,-87.671373
2018/04/29 00:02:07,net,lan,tx,102549843,102549843,BRT,41.906481,-87.671373
2018/04/29 00:02:07,net,usb,rx,326011788,326011788,BRT,41.906481,-87.671373
2018/04/29 00:02:07,net,usb,tx,287997173,287997173,BRT,41.906481,-87.671373
```

Example 5: Get temperature sensor readings only, add `unit`, `lat`, `lon`, and remove `value_raw` and `node_id`
```
$ python3 wg_datatool.py -i dataset.csv -g temperature -o output.csv -a "sensors.unit nodes.lat nodes.lon" -c "value_raw node_id" --all_cpu
[ INFO  ] Took 0.00 seconds for input file indexing
[ INFO  ] Took 0.01 seconds for the manipulation
[ INFO  ] Took 0.00 seconds for merging output
[ INFO  ] Manipulation is completed.
[ INFO  ] took 0.00 seconds for the manipulation
$ head output.csv
timestamp,subsystem,sensor,parameter,value_hrf,lat,lon,unit
2018/04/29 00:02:07,wagman,temperatures,nc_heatsink,NA,41.906481,-87.671373,
2018/04/29 00:02:07,wagman,temperatures,ep_heatsink,NA,41.906481,-87.671373,
2018/04/29 00:02:07,wagman,temperatures,battery,NA,41.906481,-87.671373,
2018/04/29 00:02:07,wagman,temperatures,brainplate,NA,41.906481,-87.671373,
2018/04/29 00:02:07,wagman,temperatures,powersupply,NA,41.906481,-87.671373,
2018/04/29 00:02:07,wagman,htu21d,temperature,25,41.906481,-87.671373,
2018/04/29 00:07:18,wagman,temperatures,nc_heatsink,NA,41.906481,-87.671373,
2018/04/29 00:07:18,wagman,temperatures,ep_heatsink,NA,41.906481,-87.671373,
2018/04/29 00:07:18,wagman,temperatures,battery,NA,41.906481,-87.671373,
```
