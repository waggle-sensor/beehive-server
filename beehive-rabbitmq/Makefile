name = beehive-rabbitmq
image = waggle/$(name):2
include ../Makefile.service

deploy:
	-docker network create $(BEEHIVE_DOCKER_NETWORK)
	-docker rm -f $(name)
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

setup:
	@docker exec -ti beehive-rabbitmq rabbitmqctl status > /dev/null

	$(eval ADMIN_PASSWORD := $(shell bash -c 'read -s -p "Enter RabbitMQ admin password: " pwd; echo $$pwd'))
	@echo

	-docker exec -ti $(name) rabbitmqctl add_user admin $(ADMIN_PASSWORD)
	-docker exec -ti $(name) rabbitmqctl set_user_tags admin administrator
	-docker exec -ti $(name) rabbitmqctl set_permissions admin ".*" ".*" ".*"

	-docker exec -ti $(name) rabbitmqctl add_user node waggle
	-docker exec -ti $(name) rabbitmqctl set_permissions node "pull-images" ".*" "pull-images"

	-docker exec -ti $(name) rabbitmqctl add_user server waggle
	-docker exec -ti $(name) rabbitmqctl set_permissions server ".*" ".*" ".*"

	-docker exec -ti $(name) rabbitmqctl add_user router router
	-docker exec -ti $(name) rabbitmqctl set_permissions router ".*" ".*" ".*"

	-docker exec -ti $(name) rabbitmqctl add_user loader_raw waggle
	-docker exec -ti $(name) rabbitmqctl set_permissions router ".*" ".*" ".*"

	-docker exec -ti $(name) rabbitmqctl add_user loader_raw waggle
	-docker exec -ti $(name) rabbitmqctl set_permissions loader_raw "^db-raw$$" "^$$" "^db-raw$$"
