# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-rabbitmq
image = waggle/$(name):2
include ../Makefile.service

deploy: startnetwork rm
	
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-e RABBITMQ_NODENAME=rabbitmq \
		-v $(BEEHIVE_ROOT)/rabbitmq/:/var/lib/rabbitmq/:rw \
		-v $(BEEHIVE_ROOT)/log/rabbitmq/:/var/log/rabbitmq/:rw \
		-v $(BEEHIVE_ROOT)/waggle/SSL:/usr/lib/waggle/SSL/:ro \
		-p 23181:5671 \
		-p 127.0.0.1:15673:15672 \
		--hostname rabbitmq \
		--network-alias rabbitmq \
		--name $(name) \
		$(image)
	

# removed localhost amqp port
# -p 127.0.0.1:5672:5672 \
# removed admin port by default
# -p 15671:15671 \
