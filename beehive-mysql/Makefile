name = beehive-mysql
image = mysql:5.7.10

deploy:
	docker network create beehive || true
	docker rm -f $(name) || true
	docker run \
		--detach \
		--net beehive \
		--restart=always \
		-v /mnt/mysql/datadir:/var/lib/mysql \
		-e MYSQL_ROOT_PASSWORD=waggle \
		-e MYSQL_DATABASE=waggle \
		-e MYSQL_USER=waggle \
		-e MYSQL_PASSWORD=waggle \
		-p 127.0.0.1:3306:3306 \
		--name $(name) \
		$(image)

rm:
	docker rm -f $(name)
