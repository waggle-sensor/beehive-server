## Current Server: 
### Beehive1: 1

```
Base OS: CentOS Linux release 7.2.1511 (Core)
Kernel: Linux beehive1.mcs.anl.gov 3.10.0-327.10.1.el7.x86_64 #1 SMP Tue Feb 16 17:03:50 UTC 
        2016 x86_64 x86_64 x86_64 GNU/Linux
Public IP: 40.221.47.67 (67.47.221.140.in-addr.arpa	name = beehive1.mcs.anl.gov.)
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











### Beehive2: 

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
