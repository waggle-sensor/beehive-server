name = beehive-message-router
image = waggle/$(name)
include ../Makefile.service

deploy: build
	-docker network create $(BEEHIVE_DOCKER_NETWORK)
	-docker rm -f $(name)
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		--name $(name) \
		$(image)
