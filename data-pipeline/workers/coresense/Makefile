build:
	docker rm -f beehive-worker-coresense || true
	docker rmi -f waggle/beehive-worker-coresense || true
	docker build -t waggle/beehive-worker-coresense .

start:
	systemctl start beehive-worker-coresense

stop:
	systemctl stop beehive-worker-coresense

restart:
	systemctl restart beehive-worker-coresense

logs:
	journalctl -f -u beehive-worker-coresense

run:
	echo 'running...'
	docker rm -f beehive-worker-coresense || true
	docker run -ti --rm  --name  beehive-worker-coresense  --net beehive waggle/beehive-worker-coresense

bash:
	echo 'bashing...'
	docker run -ti --rm  --name  beehive-worker-coresense  --net beehive waggle/beehive-worker-coresense bash

