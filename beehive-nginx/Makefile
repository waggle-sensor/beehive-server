name = beehive-nginx
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
		-p 80:80 \
		--name $(name) \
		$(image)

rm:
	docker rm -f $(name)
