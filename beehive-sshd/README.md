

# Beehive SSH

SSH server to accept reverse ssh tunnel connections from waggle nodes.

Build image:
```bash
docker build -t waggle/beehive-sshd .
```

Start container:
```bash
docker rm -f beehive-sshd
[ ! -z "$DATA" ] && \
docker run -ti --name beehive-sshd \
    -p 20022:22 \
    -v ${DATA}/waggle/SSL/nodes/:/usr/lib/waggle/SSL/nodes/ \
    waggle/beehive-sshd
```

The directory /usr/lib/waggle/SSL/nodes/ should contain an authorized_keys file with the public keys of the waggle nodes.
