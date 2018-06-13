BEEHIVE_ROOT?=/mnt
BEEHIVE_DOCKER_NETWORK?=beehive

name = beehive-sshd
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
		-p 20022:22 \
		-v ${BEEHIVE_ROOT}/ssh_keys/:/usr/lib/waggle/ssh_keys/:ro \
		-v ${BEEHIVE_ROOT}/waggle/SSL/:/usr/lib/waggle/SSL/ \
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
