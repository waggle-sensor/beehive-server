## Top Level Architecture:

Beehive is made up of many processes running in several *docker containers* -

```
beehive1:~$ docker ps
$ docker ps
CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS              PORTS                                                                                                         NAMES
a3c70587de38        waggle/beehive-worker-coresense   "python ./worker.py"     4 weeks ago         Up 36 hours                                                                                                                       beehive-worker-coresense
622f42fef4cf        waggle/beehive-flask              "gunicorn -w 5 -b 0.0"   4 weeks ago         Up 4 weeks                                                                                                                        beehive-flask
b9f4aab8fdbb        waggle/beehive-logger             "python ./logger.py"     6 weeks ago         Up 2 days                                                                                                                         beehive-logger
ba6d39f80c01        waggle/beehive-nginx              "nginx -g 'daemon off"   4 months ago        Up 4 weeks          0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp                                                                      beehive-nginx
d31d4612ca95        waggle/beehive-plenario-sender    "python3 plenario-sen"   4 months ago        Up 3 days                                                                                                                         beehive-plenario-sender
34469543b54e        waggle/beehive-loader-raw         "python ./loader.py"     5 months ago        Up 12 hours                                                                                                                       beehive-loader-raw
b1295a350f62        waggle/beehive-sshd               "/usr/sbin/sshd -D -e"   5 months ago        Up 4 weeks          0.0.0.0:20022->22/tcp                                                                                         beehive-sshd
29d66deb57af        waggle/beehive-cert               "python ./cert-serve."   5 months ago        Up 4 weeks          127.0.0.1:24181->80/tcp                                                                                       beehive-cert
ee641aa2cac4        mysql:5.7.10                      "/entrypoint.sh mysql"   5 months ago        Up 4 weeks          127.0.0.1:3306->3306/tcp                                                                                      beehive-mysql
fdd94d0688c1        cassandra:3.2                     "/docker-entrypoint.s"   5 months ago        Up 4 weeks          7000-7001/tcp, 7199/tcp, 9160/tcp, 127.0.0.1:9042->9042/tcp                                                   beehive-cassandra
3e59e3ca8455        waggle/beehive-rabbitmq           "/docker-entrypoint.s"   5 months ago        Up 4 weeks          4369/tcp, 0.0.0.0:15671->15671/tcp, 5671/tcp, 25672/tcp, 127.0.0.1:5672->5672/tcp, 0.0.0.0:23181->23181/tcp   beehive-rabbitmq

```

## Data Flow:

### 1. Inflow from Nodes: [beehive-rabbitmq container]

Node shovels data into beehive.

Node Side: https://github.com/waggle-sensor/nodecontroller/blob/master/etc/rabbitmq/rabbitmq.config

Server Side: https://github.com/waggle-sensor/beehive-server/tree/master/beehive-rabbitmq

_Config? How are the exchange and raw-queue linked?_

### 2. Data pushed into RAW database [beehive-cassandra container]

Take from data_raw queue and push into cassandra.

https://github.com/waggle-sensor/beehive-server/tree/master/beehive-loader-raw
https://github.com/waggle-sensor/beehive-server/blob/master/beehive-loader-raw/loader.py

into sensor_data_raw table


https://github.com/waggle-sensor/beehive-server/tree/master/beehive-cassandra

Cassandra is unclear. (Does this mean the manual step where you run the CQL to setup the keyspace and tables is unclear?)

### 3. Data pushed into HRF database

### 4. Data exports:

  1. Hourly

  Systemd timer on beehive:

  /etc/systemd/system/refresh-datasets.service
```  
rajesh@beehive1:~$ cat /etc/systemd/system/refresh-datasets.service
[Unit]
Description=Refresh datasets

[Service]
Type=oneshot
WorkingDirectory=/homes/moose/beehive-server/data-exporter
ExecStart=/homes/moose/beehive-server/data-exporter/refresh-datasets.sh
```


  /etc/systemd/system/refresh-datasets.timer
  ```
  rajesh@beehive1:~$ cat /etc/systemd/system/refresh-datasets.timer
[Unit]
Description=Refresh datasets hourly

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

  https://github.com/waggle-sensor/beehive-server/blob/master/data-exporter/export-decoded-datasets-csv




  2. Monthly
  3. Yearly

  rsync-mcs timer is in here ...
  ```
  refresh-datasets.timer  - 60 Min
  refresh-live-nodes.timer  - 1 Min

  refresh-recent-datasets.timer  - 5 Min

  sync-datasets-to-mcs.timer  - 15 Min
  sync-static-to-mcs.time - 5 Min
  ```

  ## Notes:

### Registration and Setup
* waggle/beehive-cert

### Management
* waggle/beehive-sshd
* mysql:5.7.10

### Beehive Data Ingest and Storage
* waggle/beehive-rabbitmq
* waggle/beehive-loader-raw
* cassandra:3.2

### Depricate
* waggle/beehive-worker-coresense
* waggle/beehive-logger
* waggle/beehive-nginx
* waggle/beehive-plenario-sender

## Scripts:
Location: beehive1:/homes/moose/beehive-server/data-exporter$
</br>
GitHub Location:
```
build-index: templates index and node pages
compress-datasets: gzips all .csv dataset files

export-datasets: writes raw dataset csv files
export-decoded-datasets-csv: decodes raw dataset and writes as csv file per nodeID / date
export-decoded-datasets-json: decodes raw dataset and writes as json file per nodeID / date
export-recent-datasets-csv: decodes last 15m of data across all nodes and write single csv, individual recent csv per node and compresses them
export-recent-datasets-csv.py: script that actually does the work for export-recent-datasets-csv

filter-last-3-days: filter output of list datasets to only include last 3 days
filter-last-day: filter output of list datasets to only include last 24h
filter-last-month: filter output of list datasets to only include last month
filter-last-week: filter output of list datasets to only include last week

list-datasets: lists distinct partition keys from sensor_data_raw in cassandra

pipeline.py: main decoder module. small

update-task.sh: depricate
refresh-datasets.sh: depricate

datasets: dataset files
static: statically generated pages
templates: index / page templates for static site generation

requirements.txt: python requirements file
datasets.index: just output from a list-datasets command

*** deprecated scripts. some were just scratchpads for things i never used
export-raw: test to see if i could run a cross compile a go version of the raw dataset csv exporter
bulk-export: was an old test of doing a multithreaded export decode csv
export-metrics:
pull-recent:
test-metrics:
```
