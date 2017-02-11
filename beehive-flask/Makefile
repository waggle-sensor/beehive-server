image = waggle/beehive-flask
container = beehive-flask

build:
	docker build -t $(image) .

start:
	systemctl start $(container)

stop:
	systemctl stop $(container)

restart:
	systemctl restart $(container)

logs:
	journalctl -f -u $(container)

clean:
	docker rm -f $(container)
	docker rmi -f $(image)

run:
	docker run -ti --rm --name $(container) -p 5000:5000 --net beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/ $(image)

bash:
	docker run -ti --rm --name $(container) -p 5000:5000 --net beehive -v /root/git/beehive-server/beehive-flask/:/usr/lib/waggle/beehive-server/beehive-flask/ $(image) bash
