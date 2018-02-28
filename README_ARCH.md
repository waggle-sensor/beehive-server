## Current Server:
### Beehive1:

```
Base OS: CentOS Linux release 7.2.1511 (Core)
Kernel: Linux beehive1.mcs.anl.gov 3.10.0-327.10.1.el7.x86_64 #1 SMP Tue Feb 16 17:03:50 UTC
        2016 x86_64 x86_64 x86_64 GNU/Linux
Public IP: `40.221.47.67 (67.47.221.140.in-addr.arpa	name = beehive1.mcs.anl.gov.)
```

#### FS of Beehive:
```
/dev/mapper/centos_beehive1-root on / type xfs (rw,relatime,seclabel,attr2,inode64,noquota)
/dev/vda1 on /boot type xfs (rw,relatime,seclabel,attr2,inode64,noquota)
```

_All the data is in /mnt which is **not** a separately mounted partition, but part of root._ - Is root of Beehive backed up? If so how often?

All the Beehive processess are run either in docker containers or as jobs directly on the base Cent OS.


##### FS Usage (27 Feb 2017): Top Users
```
55G    /

    23G    /var
        17G    /var/lib
            17G    /var/lib/docker    
                16G    /var/lib/docker/devicemapper
                    16G    /var/lib/docker/devicemapper/devicemapper
        5.4G    /var/log

    21G    /mnt
        12G    /mnt/rabbitmq
            12G    /mnt/rabbitmq/data
                12G    /mnt/rabbitmq/data/mnesia
                    12G    /mnt/rabbitmq/data/mnesia/rabbitmq
                    12G    /mnt/rabbitmq/data/mnesia/rabbitmq/queues
                        5.4G    /mnt/rabbitmq/data/mnesia/rabbitmq/queues/3KKHZI9SX6T8Q78UNERI1H2W1
                        2.0G    /mnt/rabbitmq/data/mnesia/rabbitmq/queues/CLRGSG3BEMCB4E5GRS63XRK0V
                        1.6G    /mnt/rabbitmq/data/mnesia/rabbitmq/queues/ACZI56741375WMFLVFPQSXZ67
                        1.3G    /mnt/rabbitmq/data/mnesia/rabbitmq/queues/1JE88H3ZUXZ2PM8VCY1Z7TVDP
                        1.3G    /mnt/rabbitmq/data/mnesia/rabbitmq/queues/1M6BCTH8SNGEKZL68LZBPMWQL

        7.4G    /mnt/cassandra
            7.1G    /mnt/cassandra/data
                7.1G    /mnt/cassandra/data/waggle
                    4.5G    /mnt/cassandra/data/waggle/sensor_data_raw-6a36efb090be11e68f941fe22eacf844
                    2.6G    /mnt/cassandra/data/waggle/sensor_data-9abd35e0c44f11e59521091830ac5256


        1.3G    /mnt/beehive
            1.3G    /mnt/beehive/node-logs


    7.4G    /homes
        7.1G    /homes/moose
            6.8G    /homes/moose/beehive-server
                6.8G    /homes/moose/beehive-server/data-exporter
                    6.8G    /homes/moose/beehive-server/data-exporter/datasets
                        6.8G    /homes/moose/beehive-server/data-exporter/datasets/2

    2.3G    /usr
```


#### Docker:

##### Version:
```
Client:
 Version:      1.10.2
 API version:  1.22
 Go version:   go1.5.3
 Git commit:   c3959b1
 Built:        Mon Feb 22 16:16:33 2016
 OS/Arch:      linux/amd64

Server:
 Version:      1.10.2
 API version:  1.22
 Go version:   go1.5.3
 Git commit:   c3959b1
 Built:        Mon Feb 22 16:16:33 2016
 OS/Arch:      linux/amd64
```
##### Containers:
```
1. waggle/beehive-worker-coresense
2. waggle/beehive-flask
3. waggle/beehive-logger
4. waggle/beehive-nginx
5. waggle/beehive-plenario-sender
6. waggle/beehive-loader-raw
7. waggle/beehive-sshd
8. waggle/beehive-cert
9. mysql:5.7.10
10. cassandra:3.2
11. waggle/beehive-rabbitmq
```

##### Where are the docker images created?

**Base_Dir** is root of the [beehive-server](https://github.com/waggle-sensor/beehive-server) repo.  

Some images are generated using the Dockerfile in their respective directories -
`make build` and `make deploy`
```
[Base_Dir]/beehive-loader-decoded/Dockerfile
[Base_Dir]/beehive-sshd/Dockerfile
[Base_Dir]/beehive-nginx/Dockerfile
[Base_Dir]/beehive-cert/Dockerfile
[Base_Dir]/beehive-worker-alphasense/Dockerfile
[Base_Dir]/beehive-loader/Dockerfile
[Base_Dir]/beehive-flask/Dockerfile
[Base_Dir]/beehive-loader-raw/Dockerfile
[Base_Dir]/beehive-plenario-sender/Dockerfile
[Base_Dir]/beehive-worker-gps/Dockerfile
[Base_Dir]/beehive-log-saver/Dockerfile
[Base_Dir]/beehive-worker-coresense/Dockerfile
[Base_Dir]/beehive-queue-to-mysql/Dockerfile
[Base_Dir]/beehive-rabbitmq/Dockerfile
```

#### Cassandra:

1. Docker Container: cassandra:3.2
	* This image is pulled from the public docker image repo? (Need to confirm)
	* The file here configures the container (Makefile.beehive1 - We need to understand why we have two MakeFiles in that directory) - [Makefile](https://github.com/waggle-sensor/beehive-server/blob/master/beehive-cassandra/Makefile.beehive1)



##### What do we have in Cassandra on the FS?
```
[Tue Feb 27 10:43:50 root@beehive1:/mnt/cassandra/data/waggle ] $ du -sc * | sort -k 1 -n

0	abc-624f05e090c211e68f941fe22eacf844
0	admin_messages-8ab478e07c2b11e68f941fe22eacf844
0	admin_messages-940dafb07c5811e68f941fe22eacf844
0	admin_messages-dfbc3a807c5811e68f941fe22eacf844
0	admin_messages-f605b35090c311e68f941fe22eacf844
0	node_datasets-5e301d80933911e782cc6b087c4d7187
0	node_datasets-a1f7d420933611e782cc6b087c4d7187
0	node_last_update-264f3610963411e68f941fe22eacf844
0	node_last_update-75690590961711e68f941fe22eacf844
0	node_last_update-7a1298d0960911e68f941fe22eacf844
0	node_last_update-8cb93120961711e68f941fe22eacf844
0	node_last_update-91ee3db0961811e68f941fe22eacf844
0	node_last_update-c9c2a650961711e68f941fe22eacf844
0	raw_sensor_log-77a602f0008c11e890843184f0338630
0	registration_log-9a777a50c44f11e59521091830ac5256
0	sensor_data_decoded-8642c6e07c2b11e68f941fe22eacf844
0	sensor_data_decoded-93ebcfd07c5811e68f941fe22eacf844
0	sensor_data_decoded-dfac34f07c5811e68f941fe22eacf844
0	sensor_data_decoded-e2381ed090c311e68f941fe22eacf844
0	sensor_data_raw-7ec841b07c2b11e68f941fe22eacf844
0	sensor_data_raw-93d7d2a07c5811e68f941fe22eacf844
0	sensor_data_raw-df99be607c5811e68f941fe22eacf844
0	sensor_data_ttl-9029c1f0c54111e59521091830ac5256
0	sensor_data_ttl-9afd9a40c44f11e59521091830ac5256
0	sensor_data_ttl-d8932620c53c11e59521091830ac5256
0	test_decoded-365b9b40cc9711e692721fe22eacf844
4	raw_sensor_log-ff23f1c0008b11e890843184f0338630
4	sensor_data_raw_log-97a24b50008b11e890843184f0338630
40	message_data-f7fe65d099be11e791a46b087c4d7187
40	nodes_last_log-92f5ed10f09611e6839f3b370c0fef00
40	nodes_last_ssh-930de1e0f09611e6839f3b370c0fef00
76	nodes_last_data-91be5770f09611e6839f3b370c0fef00
112	nodes-9a216b10c44f11e59521091830ac5256
112	nodes_last_update-40143230963411e68f941fe22eacf844
180	metric_data-433e5450999311e791a46b087c4d7187
64180	sensor_data_raw-478d571090be11e68f941fe22eacf844
2632020	sensor_data-9abd35e0c44f11e59521091830ac5256
4710712	sensor_data_raw-6a36efb090be11e68f941fe22eacf844

```
##### what do we have in the Cassandra DB - Tables?
_Command:_ `/bin/beehive-cqlsh`

```
#!/bin/sh
docker exec -ti beehive-cassandra cqlsh -k waggle
```

First open prompt using /bin/beehive-cqlsh
```
Connected to Test Cluster at 127.0.0.1:9042.
[cqlsh 5.0.1 | Cassandra 3.2.1 | CQL spec 3.4.0 | Native protocol v4]
Use HELP for help.
cqlsh:waggle> DESCRIBE tables;                         

1. sensor_data
2. sensor_data_raw  
3. nodes  
```

#### Table Details:
**1. sensor_data:** (This is where the old ASCII sensor data from the old nodes went. These should be early 2015 to mid-2017)
```
cqlsh:waggle> DESCRIBE TABLE sensor_data ;

CREATE TABLE waggle.sensor_data (
    node_id ascii,
    date ascii,
    plugin_id ascii,
    plugin_version int,
    plugin_instance ascii,
    timestamp timestamp,
    sensor ascii,
    data list<ascii>,
    sensor_meta ascii,
    PRIMARY KEY ((node_id, date), plugin_id, plugin_version, plugin_instance, timestamp, sensor)
) WITH CLUSTERING ORDER BY (plugin_id ASC, plugin_version ASC, plugin_instance ASC, timestamp ASC, sensor ASC)
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
```

**2. sensor_data_raw:** (This is where the current raw data from the nodes go. The data here is stored in the raw form, using the old V2 prot.)
```
cqlsh:waggle> DESCRIBE TABLE sensor_data_raw ;

CREATE TABLE waggle.sensor_data_raw (
    node_id ascii,
    date ascii,
    plugin_name ascii,
    plugin_version ascii,
    plugin_instance ascii,
    timestamp timestamp,
    parameter ascii,
    data ascii,
    ingest_id int,
    PRIMARY KEY ((node_id, date), plugin_name, plugin_version, plugin_instance, timestamp, parameter)
) WITH CLUSTERING ORDER BY (plugin_name ASC, plugin_version ASC, plugin_instance ASC, timestamp ASC, parameter ASC)
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
```

**3. Nodes:** (We do _not_ know what this table does or how it impacts the rest of the system, so keeping it alive for now)
```
cqlsh:waggle> DESCRIBE TABLE nodes  ;

CREATE TABLE waggle.nodes (
    node_id ascii PRIMARY KEY,
    children list<ascii>,
    name ascii,
    parent ascii,
    plugins_all set<frozen<plugin>>,
    plugins_currently set<frozen<plugin>>,
    queue ascii,
    reverse_port int,
    timestamp timestamp
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
```

#### MySQL

Stores node management and metadata.

##### Deployment

Docker container: `beehive-mysql`

Docker image: `mysql:5.7.10`

Listening: `127.0.0.1:3306`

Admin User: `waggle`

Admin Password: `waggle`

Default Database `waggle`

##### Access

Use `beehive-server/bin/beehive-mysql` to connect to `waggle` database inside container.

##### Tables

Currently, have many tables (mostly unused):

```
MySQL [waggle]> show tables;
+----------------------+
| Tables_in_waggle     |
+----------------------+
| calibration          |
| hardware             |
| node_config          |
| node_management      |
| node_management0     |
| node_meta            |
| node_notes           |
| node_offline         |
| nodes                |
| nodes0               |
| nodes1               |
| nodes2               |
| nodesApril7          |
| nodes_2017_06_21     |
| nodes_2017_08_10     |
| nodes_May16_2017     |
| nodes_May3           |
| role                 |
| roles_users          |
| software             |
| ssh_status           |
| testing_groups       |
| testing_nodes        |
| testing_nodes_groups |
| user                 |
+----------------------+
```

AFAIK, `nodes` is the only table in active use. It stores management data about each node. (It does _not_ store ssh keys or certificates! Discussed in section *will add*.)

```
MySQL [waggle]> describe nodes;
+------------------+--------------+------+-----+----------+----------------+
| Field            | Type         | Null | Key | Default  | Extra          |
+------------------+--------------+------+-----+----------+----------------+
| id               | int(11)      | NO   | PRI | NULL     | auto_increment |
| node_id          | varchar(16)  | YES  |     | NULL     |                |
| project          | int(11)      | YES  | MUL | NULL     |                |
| description      | varchar(255) | YES  |     | NULL     |                |
| reverse_ssh_port | mediumint(9) | YES  |     | NULL     |                |
| hostname         | varchar(64)  | YES  |     | NULL     |                |
| hardware         | json         | YES  |     | NULL     |                |
| name             | varchar(64)  | YES  |     | NULL     |                |
| location         | varchar(255) | YES  |     | NULL     |                |
| last_updated     | timestamp    | YES  |     | NULL     |                |
| opmode           | varchar(64)  | YES  |     | testing. |                |
| groups           | varchar(128) | YES  |     |          |                |
+------------------+--------------+------+-----+----------+----------------+
12 rows in set (0.11 sec)
```

### Beehive2

```
 Host beehive-prod
  ProxyCommand ssh -q mcs nc -q0 beehive01.cels.anl.gov 22
  User moose

Host beehive-dev
  ProxyCommand ssh -q mcs nc -q0 beehive01-dev.cels.anl.gov 22
  User moose

Host beehive-test
  ProxyCommand ssh -q mcs nc -q0 beehive01-test.cels.anl.gov 22
  User moose
```
