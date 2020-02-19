# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-data-loader
image = waggle/$(name):2
include ../Makefile.service

deploy: startnetwork rm
	
	docker run \
		--detach \
		-e CASSANDRA_HOST=$(CASSANDRA_HOST) \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		--name $(name) \
		$(image)
