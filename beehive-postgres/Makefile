# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-postgres
image = waggle/$(name):1
include ../Makefile.service

deploy: ## Runs the image in detached mode
	-docker network create $(BEEHIVE_DOCKER_NETWORK)
	-docker rm -f $(name)
	docker run \
		--detach \
		--restart=always \
		-v $(BEEHIVE_ROOT)/postgres:/var/lib/postgresql \
		-e POSTGRES_PASSWORD=waggle \
		-p 5432:5432 \
		--hostname $(name) \
		--network-alias $(name) \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--name $(name) \
		$(image)

setup: ## No op
	@echo 'no op'

