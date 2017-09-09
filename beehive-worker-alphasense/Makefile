name = beehive-worker-alphasense
image = waggle/$(name)

build:
	docker build -t $(image) .

run:
	docker run --detach --net beehive --restart=on-failure:10 -e WORKER_DEPLOYMENT=/ --name $(name) $(image)

start:
	systemctl start $(name)

stop:
	systemctl stop $(name)

restart:
	systemctl restart $(name)
