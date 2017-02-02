build:
	docker rm -f beehive-worker-alphasense || true
	docker rmi -f waggle/beehive-worker-alphasense || true
	docker build -t waggle/beehive-worker-alphasense .

start:
	systemctl start beehive-worker-alphasense

stop:
	systemctl stop beehive-worker-alphasense

restart:
	systemctl restart beehive-worker-alphasense

logs:
	journalctl -f -u beehive-worker-alphasense

run:
	echo 'running...'
	docker rm -f beehive-worker-alphasense || true
	docker run -ti --rm  --name  beehive-worker-alphasense  --net beehive waggle/beehive-worker-alphasense

bash:
	echo 'bashing...'
	docker run -ti --rm  --name  beehive-worker-alphasense  --net beehive waggle/beehive-worker-alphasense bash

