name = beehive-nginx
image = waggle/$(name)

deploy: build
	-docker network create $(BEEHIVE_DOCKER_NETWORK)
	-docker rm -f $(name)
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-p 80:80 \
		-v $(BEEHIVE_ROOT)/www:/www:ro \
		--name $(name) \
		$(image)

include ../Makefile.service
