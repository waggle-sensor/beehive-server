build:
	#docker rm -f beehive-flask
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
	#docker rm -f beehive-flask
	echo 'running...'
	#docker run -ti --rm  --name beehive-flask  -p8183:80 --network=beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/  waggle/beehive-flask
	docker run -ti --rm  --name beehive-flask  -p5000:5000 --network=beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/  waggle/beehive-flask


bash:
	echo 'bashing...'
	#docker rm -f beehive-flask
	docker run -ti --rm  --name beehive-flask  -p5000:5000 --network=beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/  waggle/beehive-flask  bash
