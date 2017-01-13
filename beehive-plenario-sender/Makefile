build:
	docker rm -f beehive-plenario-sender || echo 'rm failed'
	docker rmi -f waggle/beehive-plenario-sender || echo 'rmi failed'
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
	docker rm -f beehive-plenario-sender || echo 'rm failed'
	#docker run -ti --rm  --name beehive-plenario-sender --net beehive -v  /root/git/beehive-server/beehive-plenario-sender/:/usr/lib/waggle/beehive-server/beehive-plenario-sender/  waggle/beehive-plenario-sender bash -c 'pwd; ls -l'
	docker run -ti --rm  --name beehive-plenario-sender --net beehive -v  /root/git/beehive-server/beehive-plenario-sender/:/usr/lib/waggle/beehive-server/beehive-plenario-sender/  -v /mnt/beehive:/mnt/beehive -v /mnt/waggle:/mnt/waggle waggle/beehive-plenario-sender 

bash:
	echo 'bashing...'
	docker run -ti --rm  --name beehive-plenario-sender --net beehive -v /root/git/beehive-server/beehive-plenario-sender/:/usr/lib/waggle/beehive-server/beehive-plenario-sender/  waggle/beehive-plenario-sender  bash
