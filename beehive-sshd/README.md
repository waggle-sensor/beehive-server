

# Beehive SSH

SSH server to accept reverse ssh tunnel connections from waggle nodes.

Build image:
```bash
docker rm -f beehive-sshd
docker rmi waggle/beehive-sshd
docker pull waggle/beehive-server
docker build -t waggle/beehive-sshd .
```

Start container:
```bash
docker rm -f beehive-sshd
[ ! -z "$DATA" ] && \
docker run -ti --name beehive-sshd \
    --net beehive \
    -p 20022:22 \
    -v ${DATA}/ssh_keys/:/usr/lib/waggle/ssh_keys/ \
    -v ${DATA}/waggle/SSL/nodes/:/usr/lib/waggle/SSL/nodes/ \
    waggle/beehive-sshd
```

The directory /usr/lib/waggle/SSL/nodes/ should contain an authorized_keys file with the public keys of the waggle nodes.

## SSH via tunnel

To find port use the beehive API:

http://beehive1.mcs.anl.gov/api/1/nodes/


ssh into node:
```bash
docker exec -ti beehive-sshd ssh -i /usr/lib/waggle/ssh_keys/id_rsa_waggle_aot waggle@localhost -p <PORT>
```

## Open ports

```bash
docker exec -ti beehive-sshd netstat -tulpn
```
