# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

BEEHIVE_ROOT?=/mnt/storage
SERVICES = mysql cert postgres rabbitmq message-router data-loader sshd nginx

.PHONY: help

help:
	@echo "USAGE"
	@echo "make [target]"
	@echo ""
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
	@echo ""

build: ## Sets up up SSH keys dir and builds the Docker images for the Beehive services
	-mkdir -p $(BEEHIVE_ROOT)/ssh_keys
	cp ssh/id_rsa_waggle_aot_registration.pub $(BEEHIVE_ROOT)/ssh_keys/
	cd $(BEEHIVE_ROOT)/beehive-server/beehive-core; make build
	$(foreach service, $(SERVICES), cd $(BEEHIVE_ROOT)/beehive-server/beehive-$(service) && make build;)

run: ## Runs the Docker images for the Beehive services
	$(foreach service, $(SERVICES), cd $(BEEHIVE_ROOT)/beehive-server/beehive-$(service) && make deploy;)

configure: ## Runs the setup/init scripts for the running Beehive services
	$(foreach service, $(SERVICES), cd $(BEEHIVE_ROOT)/beehive-server/beehive-$(service) && make setup;)

stop: ## Stops the running Beehive services
	$(foreach service, $(SERVICES), cd $(BEEHIVE_ROOT)/beehive-server/beehive-$(service) && make stop;)

snapshot: ## Tags the Beehive services with the current date
	$(foreach service, $(SERVICES), cd $(BEEHIVE_ROOT)/beehive-server/beehive-$(service) && make stop;)
