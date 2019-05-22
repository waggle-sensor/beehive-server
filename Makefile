# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

BEEHIVE_ROOT?=/mnt/storage
SERVICES:=$(wildcard ./beehive-*)

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
	$(foreach service, $(SERVICES), cd $(service) && make build && cd ..;)

run: ## Runs the Docker images for the Beehive services
	$(foreach service, $(SERVICES), cd $(service) && make deploy && cd ..;)

configure: ## Runs the setup/init scripts for the running Beehive services
	$(foreach service, $(SERVICES), cd $(service) && make setup && cd ..;)

stop: ## Stops the running Beehive services
	$(foreach service, $(SERVICES), cd $(service) && make stop && cd ..;)

snapshot: ## Tags the Beehive services with the current date
	$(foreach service, $(SERVICES), cd $(service) && make stop && cd ..;)
