build:
	docker rm -f beehive-flask
	docker rmi -f waggle/beehive-flask
	docker build -t waggle/beehive-flask .

start:
	systemctl start beehive-flask

stop:
	systemctl stop beehive-flask

restart:
	systemctl restart beehive-flask

logs:
	journalctl -f -u beehive-flask

run:
	echo 'running...'
	docker rm -f beehive-flask || echo 'docker rm -f beehive-flask failed'
	docker run -ti --rm  --name beehive-flask  -p 5000:5000 --net beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/  waggle/beehive-flask

bash:
	echo 'bashing...'
	docker run -ti --rm  --name beehive-flask  -p 5000:5000 --net beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/  waggle/beehive-flask  bash
