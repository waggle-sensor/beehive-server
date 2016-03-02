

# Beehive SSH

SSH server to accept reverse ssh tunnel connections from waggle nodes.

Build image:
```bash
docker build -t waggle/beehive-ssh ./docker/
```

Start container:
```bash
docker rm -f beehive-ssh
docker pull waggle/beehive-server:latest
[ ! -z "$DATA" ] && \
docker run -ti --name beehive-ssh \
    -p 20022:22 \
    -v ${DATA}/waggle/SSL/nodes/:/usr/lib/waggle/SSL/nodes/ \
    waggle/beehive-ssh
```

The directory /usr/lib/waggle/SSL/nodes/ should contain an authorized_keys file with the public keys of the waggle nodes.
