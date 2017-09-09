name = beehive-rabbitmq
image = rabbitmq:3.5.6

deploy:
	docker network create beehive || true
	docker rm -f $(name) || true
	docker run \
		--detach \
		--net beehive \
		--restart=always \
		-e RABBITMQ_NODENAME=$(name) \
		-v /mnt/rabbitmq/config/:/etc/rabbitmq \
		-v /mnt/rabbitmq/data/:/var/lib/rabbitmq/:rw \
		-v /mnt/waggle/SSL:/usr/lib/waggle/SSL/:ro \
		-p 127.0.0.1:5672:5672 \
		-p 23181:23181 \
		-p 15671:15671 \
		--hostname $(name) \
		--name $(name) \
		$(image)

rm:
	docker rm -f $(name)
