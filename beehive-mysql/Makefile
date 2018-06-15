name = beehive-mysql
image = waggle/$(name)

run:
	docker network create $(BEEHIVE_DOCKER_NETWORK) || true
	docker rm -f $(name) || true
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-v $(BEEHIVE_ROOT)/mysql:/var/lib/mysql \
		-e MYSQL_ROOT_PASSWORD=waggle \
		-e MYSQL_DATABASE=waggle \
		-e MYSQL_USER=waggle \
		-e MYSQL_PASSWORD=waggle \
		-p 127.0.0.1:3306:3306 \
		--hostname beehive-mysql \
		--network-alias beehive-mysql \
		--name $(name) \
		$(image)

include ../Makefile.service
