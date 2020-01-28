# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-nginx
image = nginx:1.17
include ../Makefile.service

deploy: startnetwork rm
	#@test -n "$(BEEHIVE_ROOT)" || bash -c 'echo "BEEHIVE_ROOT not defined" ; exit 1' 
	@test -n "$(BEEHIVE_DOCKER_NETWORK)" || bash -c 'echo "BEEHIVE_DOCKER_NETWORK not defined" ; exit 1' 
	
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-p 80:80 \
		-v `pwd`/api_nodes_access.whitelist:/etc/nginx/app/api_nodes_access.whitelist:ro \
		-v `pwd`/upstreams:/etc/nginx/upstreams/:ro \
		-v `pwd`/locations:/etc/nginx/locations/:ro \
		-v `pwd`/nginx.conf:/etc/nginx/nginx.conf:ro \
		-v `pwd`/beehive.conf:/etc/nginx/conf.d/default.conf:ro \
		--name $(name) \
		$(image)

# -v $(BEEHIVE_ROOT)/www:/www:ro \
