# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-mysql
image = mysql:8.0.19
include ../Makefile.service

deploy: startnetwork rm
	
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-v $(PWD)/init.sql:/docker-entrypoint-initdb.d/init.sql \
		-v $(BEEHIVE_ROOT)/mysql:/var/lib/mysql \
		-e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) \
		-e MYSQL_DATABASE=$(MYSQL_DB) \
		-e MYSQL_USER=$(MYSQL_USER) \
		-e MYSQL_PASSWORD=$(MYSQL_PASSWD) \
		--hostname beehive-mysql \
		--network-alias beehive-mysql \
		--name $(name) \
		$(image)

#-p 127.0.0.1:3306:3306 \
