build:
	docker rm -f beehive-plenario-sender  && echo 'rm succeeded'
	docker rmi -f waggle/beehive-plenario-sender  && echo 'rmi succeeded'
	docker build -t waggle/beehive-plenario-sender .

start:
	systemctl start beehive-plenario-sender

stop:
	systemctl stop beehive-plenario-sender

restart:
	systemctl restart beehive-plenario-sender

logs:
	journalctl -f -u beehive-plenario-sender

run:
	echo 'running...'
	docker rm -f beehive-plenario-sender && echo 'rm succeeded'
	docker run -ti --rm  --name beehive-plenario-sender  -p 5000:5000 --net beehive -v  /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-plenario-sender/  waggle/beehive-plenario-sender

bash:
	echo 'bashing...'
	docker run -ti --rm  --name beehive-plenario-sender  -p 5000:5000 --net beehive -v /root/git/beehive-server/beehive-plenario-sender/:/usr/lib/waggle/beehive-server/beehive-plenario-sender/  waggle/beehive-plenario-sender  bash
