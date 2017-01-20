build:
	docker rm -f beehive-queue-to-mysql || echo 'no container to rm'
	docker rmi -f waggle/beehive-queue-to-mysql || echo 'no docker image to rm'
	docker build -t waggle/beehive-queue-to-mysql .

start:
	systemctl start beehive-queue-to-mysql

stop:
	systemctl stop beehive-queue-to-mysql

restart:
	systemctl restart beehive-queue-to-mysql

logs:
	journalctl -f -u beehive-queue-to-mysql

run:
	echo 'running...'
	docker rm -f beehive-queue-to-mysql || echo 'no container to rm'
	docker run -ti --rm  --name beehive-queue-to-mysql  -p 5000:5000 --net beehive -v /root/git/beehive-server/beehive-queue-to-mysql/:/usr/lib/waggle/beehive-server/beehive-queue-to-mysql/  waggle/beehive-queue-to-mysql

bash:
	echo 'bashing...'
	docker run -ti --rm  --name beehive-queue-to-mysql  -p 5000:5000 --net beehive -v /root/git/beehive-server/beehive-queue-to-mysql/:/usr/lib/waggle/beehive-server/beehive-queue-to-mysql/  waggle/beehive-queue-to-mysql  bash
