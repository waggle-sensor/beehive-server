build:
	docker rm -f beehive-worker-gps-sense || true
	docker rmi -f waggle/beehive-worker-gps-sense || true
	docker build -t waggle/beehive-worker-gps-sense .

start:
	systemctl start beehive-worker-gps-sense

stop:
	systemctl stop beehive-worker-gps-sense

restart:
	systemctl restart beehive-worker-gps-sense

logs:
	journalctl -f -u beehive-worker-gps-sense

run:
	echo 'running...'
	docker rm -f beehive-worker-gps-sense || true
	docker run -ti --rm  --name  beehive-worker-gps-sense  --net beehive waggle/beehive-worker-gps-sense

bash:
	echo 'bashing...'
	docker run -ti --rm  --name  beehive-worker-gps-sense  --net beehive waggle/beehive-worker-gps-sense bash

