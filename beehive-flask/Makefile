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
	#docker run -ti --rm  --name beehive-flask  -p 8183:80 --net beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/  waggle/beehive-flask
	docker run -ti --rm  --name beehive-flask  -p 5000:5000 --net beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/  waggle/beehive-flask

run2:
	#docker rm -f beehive-flask
	echo 'running...'
	#docker run -ti --rm  --name beehive-flask  -p 8183:80 --net beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/  waggle/beehive-flask
	docker run -ti --rm  --name beehive-flask  -p 5000:5000 --net beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/  waggle/beehive-flask


bash:
	echo 'bashing...'
	#docker rm -f beehive-flask
	docker run -ti --rm  --name beehive-flask  -p 5000:5000 --net beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/  waggle/beehive-flask  bash
