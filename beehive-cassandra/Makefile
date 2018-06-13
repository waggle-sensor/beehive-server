BEEHIVE_ROOT?=/mnt
BEEHIVE_DOCKER_NETWORK?=beehive

name = beehive-cassandra
image = cassandra:3

deploy:
	docker network create $(BEEHIVE_DOCKER_NETWORK) || true
	docker rm -f $(name) || true
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-v $(BEEHIVE_ROOT)/cassandra/:/var/lib/cassandra/ \
		-p 127.0.0.1:9042:9042 \
		--hostname cassandra \
		--network-alias cassandra \
		--name $(name) \
		$(image)

rm:
	docker rm -f $(name)
