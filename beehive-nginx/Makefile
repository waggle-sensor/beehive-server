BEEHIVE_ROOT?=/mnt
BEEHIVE_DOCKER_NETWORK?=beehive

name = beehive-nginx
image = waggle/$(name)

build:
	docker build -t $(image) .

deploy:
	docker network create $(BEEHIVE_DOCKER_NETWORK) || true
	docker rm -f $(name) || true
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-p 80:80 \
		--name $(name) \
		$(image)

rm:
	docker rm -f $(name)
