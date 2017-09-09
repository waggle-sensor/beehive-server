name = beehive-worker-alphasense
image = waggle/$(name)

build:
	docker build -t $(image) .

deploy:
	docker network create beehive || true
	docker rm -f $(name) || true
	docker run --detach --net beehive --restart=always -e BEEHIVE_DEPLOYMENT=/ --name $(name) $(image)

rm:
	docker rm -f $(name)

start:
	systemctl start $(name)

stop:
	systemctl stop $(name)

restart:
	systemctl restart $(name)
