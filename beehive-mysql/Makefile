# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-mysql
image = waggle/$(name):2
include ../Makefile.service

deploy: ## Runs the image in detached mode
	-docker network create $(BEEHIVE_DOCKER_NETWORK)
	-docker rm -f $(name)
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

setup: ## No op
	@echo 'no op'
