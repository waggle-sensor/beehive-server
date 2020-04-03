# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-loader-raw
image = waggle/$(name):2
include ../Makefile.service

deploy: startnetwork rm
	
	# Note that CASSANDRA_HOSTS has an "S" at the end

	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		-e "CASSANDRA_HOSTS=$(CASSANDRA_HOST)" \
		-e "RABBITMQ_HOST=$(RABBITMQ_HOST)" \
		-e "RABBITMQ_PORT=$(RABBITMQ_PORT)" \
		--restart=always \
		--name $(name) \
		$(image)
