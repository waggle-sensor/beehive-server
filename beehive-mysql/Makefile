BEEHIVE_ROOT?=/mnt
BEEHIVE_DOCKER_NETWORK?=beehive

name = beehive-mysql
image = waggle/$(name)

build:
	docker build -t $(image) .

deploy:
	docker network create $(BEEHIVE_DOCKER_NETWORK) || true
	docker rm -f $(name) || true
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-v $(BEEHIVE_ROOT)/mysql/datadir:/var/lib/mysql \
		-e MYSQL_ROOT_PASSWORD=waggle \
		-e MYSQL_DATABASE=waggle \
		-e MYSQL_USER=waggle \
		-e MYSQL_PASSWORD=waggle \
		-p 127.0.0.1:3306:3306 \
		--hostname beehive-mysql \
		--network-alias beehive-mysql \
		--name $(name) \
		$(image)

rm:
	docker rm -f $(name)
