# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

name = beehive-sshd
image = waggle/$(name):2
include ../Makefile.service

deploy: startnetwork rm
	
	docker run \
		--detach \
		--net ${BEEHIVE_DOCKER_NETWORK} \
		--restart=always \
		-p 20022:22 \
		-v ${BEEHIVE_ROOT}/ssh_keys/:/usr/lib/waggle/ssh_keys/:ro \
		-v ${BEEHIVE_ROOT}/waggle/SSL/:/usr/lib/waggle/SSL/ \
		--name $(name) \
		$(image)
