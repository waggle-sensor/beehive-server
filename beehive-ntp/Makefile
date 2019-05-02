# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-ntp
include ../Makefile.service

deploy:
	-docker network create $(BEEHIVE_DOCKER_NETWORK)
	-docker rm -f $(name)
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		--publish=123:123/udp  \
		--cap-add=SYS_NICE     \
		--cap-add=SYS_RESOURCE \
		--cap-add=SYS_TIME     \
		--name $(name) \
		cturra/ntp
