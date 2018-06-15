name = beehive-sshd
image = waggle/$(name)

deploy: build
	-docker network create ${BEEHIVE_DOCKER_NETWORK}
	-docker rm -f $(name)
	docker run \
		--detach \
		--net ${BEEHIVE_DOCKER_NETWORK} \
		--restart=always \
		-p 20022:22 \
		-v ${BEEHIVE_ROOT}/ssh_keys/:/usr/lib/waggle/ssh_keys/:ro \
		-v ${BEEHIVE_ROOT}/waggle/SSL/:/usr/lib/waggle/SSL/ \
		--name $(name) \
		$(image)

include ../Makefile.service
