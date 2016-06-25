
## Systemd unit files for all beehive server components 

Download files if not already done:
```bash
cd ~
mkdir -p git
cd git
git clone https://github.com/waggle-sensor/beehive-server.git
cd ~/git/beehive-server/systemd/
```


Enable docker.service if needed:
```bash
systemctl enable docker.service
systemctl start docker.service
systemctl status docker.service
```


Example for single unit:
```bash
cp beehive-cassandra.service /etc/systemd/system
systemctl enable beehive-cassandra.service
systemctl start beehive-cassandra.service
systemctl status beehive-cassandra.service
```

Deploy all unit files:
```bash
for service in *.service ; do
  echo "Deploy ${service}"
  rm -f /etc/systemd/system/${service}
  cp ${service} /etc/systemd/system
  systemctl enable ${service}
  systemctl start ${service}
  sleep 3
  systemctl status ${service}
done
```

## Logging

For services that do not write log files, but print to stdout and stderr, use journald to see the logs:

```bash
journalctl -f -u beehive-web
```
