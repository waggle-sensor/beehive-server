BEEHIVE_ROOT?=/mnt
BEEHIVE_DOCKER_NETWORK?=beehive

name = beehive-rabbitmq
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
		-e RABBITMQ_NODENAME=rabbitmq \
		-v $(BEEHIVE_ROOT)/rabbitmq/:/var/lib/rabbitmq/:rw \
		-v $(BEEHIVE_ROOT)/log/rabbitmq/:/var/log/rabbitmq/:rw \
		-v $(BEEHIVE_ROOT)/waggle/SSL:/usr/lib/waggle/SSL/:ro \
		-p 127.0.0.1:5672:5672 \
		-p 23181:5671 \
		-p 15671:15671 \
		--hostname rabbitmq \
		--network-alias rabbitmq \
		--name $(name) \
		$(image)

rm:
	docker rm -f $(name)

setup:
	docker exec -ti $(name) rabbitmqctl add_user admin $(shell bash -c 'read -s -p "Admin Password: " pwd; echo $$pwd') || true
	docker exec -ti $(name) rabbitmqctl set_user_tags admin administrator || true
	docker exec -ti $(name) rabbitmqctl set_permissions admin ".*" ".*" ".*" || true

	docker exec -ti $(name) rabbitmqctl add_user node waggle || true
	docker exec -ti $(name) rabbitmqctl set_permissions node "pull-images" ".*" "pull-images" || true

	docker exec -ti $(name) rabbitmqctl add_user server waggle || true
	docker exec -ti $(name) rabbitmqctl set_permissions server ".*" ".*" ".*" || true

	docker exec -ti $(name) rabbitmqctl add_user loader_raw waggle || true
	docker exec -ti $(name) rabbitmqctl set_permissions loader_raw "^db-raw$$" "^$$" "^db-raw$$" || true
