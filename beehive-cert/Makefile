name = beehive-cert
image = waggle/$(name)

build:
	docker build -t $(image) .

deploy:
	docker network create beehive || true
	docker rm -f $(name) || true
	docker run \
		--detach \
		--net beehive \
		--restart=always \
		-p 24181:80 \
		-v /mnt/ssh_keys/:/usr/lib/waggle/ssh_keys/:ro \
		-v /mnt/waggle/SSL/:/usr/lib/waggle/SSL/ \
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
