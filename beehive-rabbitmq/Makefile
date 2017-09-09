name = beehive-rabbitmq
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
		-e RABBITMQ_NODENAME=$(name) \
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

setup:
	docker exec -ti beehive-rabbitmq rabbitmqctl add_vhost production || true
	docker exec -ti beehive-rabbitmq rabbitmqctl add_vhost development || true
	docker exec -ti beehive-rabbitmq rabbitmqctl add_vhost testing || true

	docker exec -ti $(name) rabbitmqctl add_user node waggle || true
	docker exec -ti $(name) rabbitmqctl set_permissions node "pull-images" ".*" "pull-images" || true
	docker exec -ti $(name) rabbitmqctl set_permissions -p production node "^$" ".*" "^$" || true
	docker exec -ti $(name) rabbitmqctl set_permissions -p development node "^$" ".*" "^$" || true
	docker exec -ti $(name) rabbitmqctl set_permissions -p testing node "^$" ".*" "^$" || true

	docker exec -ti $(name) rabbitmqctl add_user server waggle || true
	docker exec -ti $(name) rabbitmqctl set_permissions server ".*" ".*" ".*" || true
	docker exec -ti $(name) rabbitmqctl set_permissions -p production server ".*" ".*" ".*" || true
	docker exec -ti $(name) rabbitmqctl set_permissions -p development server ".*" ".*" ".*" || true
	docker exec -ti $(name) rabbitmqctl set_permissions -p testing server ".*" ".*" ".*" || true
