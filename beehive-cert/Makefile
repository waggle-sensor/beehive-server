name = beehive-cert
image = waggle/$(name)
include ../Makefile.service

deploy:
	-docker network create $(BEEHIVE_DOCKER_NETWORK)
	-docker rm -f $(name)
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-p 127.0.0.1:24181:80 \
		-v $(BEEHIVE_ROOT)/ssh_keys/:/usr/lib/waggle/ssh_keys/:ro \
		-v $(BEEHIVE_ROOT)/waggle/SSL/:/usr/lib/waggle/SSL/ \
		--name $(name) \
		$(image)

setup:
	docker exec -ti $(name) SSL/create_certificate_authority.sh
	docker exec -ti $(name) SSL/create_server_cert.sh
