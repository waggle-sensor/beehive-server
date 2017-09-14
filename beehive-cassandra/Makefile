name = beehive-cassandra
image = cassandra:3.2

deploy:
	docker network create beehive || true
	docker rm -f $(name) || true
	docker run \
		--detach \
		--net beehive \
		--restart=always \
		-v /mnt/cassandra/:/var/lib/cassandra/ \
		-p 127.0.0.1:9042:9042 \
		--hostname cassandra \
		--network-alias cassandra \
		--name $(name) \
		$(image)

rm:
	docker rm -f $(name)
