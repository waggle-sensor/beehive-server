# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-cert
image = waggle/$(name):2
include ../Makefile.service

deploy: ## Runs the image in detached mode
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

setup: ## Sets up the SSL CA
	docker exec -ti $(name) SSL/create_certificate_authority.sh
	docker exec -ti $(name) SSL/create_server_cert.sh
