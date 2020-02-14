# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-cassandra
image = cassandra:3
include ../Makefile.service

deploy: startnetwork rm

	$(eval COUNT := $(shell docker network ls -q  -f name=$(BEEHIVE_DOCKER_NETWORK)$ | wc -l ))
	@if [ ! $(COUNT) -eq 1 ] ; then set -x ; docker network create $(BEEHIVE_DOCKER_NETWORK) ; fi

	
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-v $(BEEHIVE_ROOT)/cassandra/:/var/lib/cassandra/ \
		-v $(BEEHIVE_ROOT)/log/cassandra/:/var/log/cassandra/:rw \
		-p 127.0.0.1:9042:9042 \
		--hostname cassandra \
		--network-alias cassandra \
		--name $(name) \
		$(image)

setup:
	./init.sh
