# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-registration
image = waggle/$(name):2
include ../Makefile.service

deploy: startnetwork rm
	
	docker run \
  		--detach \
  		--net $(BEEHIVE_DOCKER_NETWORK)  \
		--restart=always \
  		-p 8184:5000 \
  		-e FLASK_ENV=development \
  		-e MYSQL_HOST="beehive-mysql" \
  		-e MYSQL_USER="waggle" \
  		-e MYSQL_PASSWD="waggle" \
  		-e MYSQL_DB="waggle" \
  		--name $(name) \
		$(image)	
