# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-cert
image = waggle/$(name):2
include ../Makefile.service

deploy: startnetwork rm
	
	docker run \
		--detach \
		--net $(BEEHIVE_DOCKER_NETWORK) \
		--restart=always \
		-p 127.0.0.1:24181:80 \
		-e MYSQL_HOST="beehive-mysql" \
  		-e MYSQL_USER="waggle" \
  		-e MYSQL_PASSWD="waggle" \
  		-e MYSQL_DB="waggle" \
		-v $(BEEHIVE_ROOT)/ssh_keys/:/usr/lib/waggle/ssh_keys/:ro \
		-v $(BEEHIVE_ROOT)/waggle/SSL/:/usr/lib/waggle/SSL/ \
		--name $(name) \
		$(image)

setup:
	docker exec -ti $(name) SSL/create_certificate_authority.sh
	docker exec -ti $(name) SSL/create_server_cert.sh
