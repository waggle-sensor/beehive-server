name = beehive-cert
image = waggle/$(name)

build:
	docker build -t $(image) .

deploy:
	docker network create ${BEEHIVE_DOCKER_NETWORK} || true
	docker rm -f $(name) || true
	docker run \
		--detach \
		--net ${BEEHIVE_DOCKER_NETWORK} \
		--restart=always \
		-p 127.0.0.1:24181:80 \
		-v ${BEEHIVE_ROOT}/ssh_keys/:/usr/lib/waggle/ssh_keys/:ro \
		-v ${BEEHIVE_ROOT}/SSL/:/usr/lib/waggle/SSL/ \
		--name $(name) \
		$(image)

rm:
	docker rm -f $(name)

start:
	docker start $(name)

stop:
	docker stop $(name)

restart:
	docker restart $(name)
