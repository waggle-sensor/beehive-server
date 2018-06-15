name = beehive-cassandra
image = cassandra:3

run:
	-docker network create $(BEEHIVE_DOCKER_NETWORK)
	-docker rm -f $(name)
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
	docker exec -i $(name) 'cqlsh' < init.cql

include ../Makefile.service
