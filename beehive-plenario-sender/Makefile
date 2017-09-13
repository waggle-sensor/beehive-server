name = beehive-plenario-sender
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
		-e AWS_ACCESS_KEY=FILL_IN \
		-e AWS_SECRET_KEY=FILL_IN \
		--name $(name) \
		$(image)

rm:
	docker rm -f $(name)

start:
	systemctl start $(name)

stop:
	systemctl stop $(name)

restart:
	systemctl restart $(name)
