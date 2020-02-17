#!/bin/bash

set -e


# This script creates users in RabbitMQ.
# It is a bit complicated because rabbitmqctl exits with an error if a user already exists.
# To avoid this we get a list of all existing users in RabbitMQ and create only those missing. 



if [ $# -lt 1 ]; then
  echo 1>&2 "$0: not enough arguments"
  exit 2
elif [ $# -gt 1 ]; then
  echo 1>&2 "$0: too many arguments"
  exit 2
fi


if [ -z ${RABBITMQ_ADMIN_PASSWORD} ] ; then
	echo "Variable RABBITMQ_ADMIN_PASSWORD not set"
	exit 1
fi


#echo "RABBITMQ_ADMIN_PASSWORD: ${RABBITMQ_ADMIN_PASSWORD}"

container_name=${1}



if [ -z ${container_name} ] ; then
	echo "Variable container_name not set"
	exit 1
fi



# wait for rabbitmq to up
docker exec -ti ${container_name} rabbitmqctl status > /dev/null

echo "Getting list of RabbitMQ users..."
unset RABBIT_USERS
set -x
RABBIT_USERS=$( for i in $(docker exec -ti ${container_name} rabbitmqctl list_users -q) ; do echo $i  ; done | grep -v "^\[" || true )
set +x

echo "Creating missing RabbitMQ users..."
# \b is matches word boundary

if [ $(echo ${RABBIT_USERS} | grep "\badmin" | wc -l | tr -d " ") -eq 0 ] ; then
	set -x
	docker exec -ti ${container_name} rabbitmqctl add_user admin ${RABBITMQ_ADMIN_PASSWORD}
	docker exec -ti ${container_name} rabbitmqctl set_user_tags admin administrator
	docker exec -ti ${container_name} rabbitmqctl set_permissions admin ".*" ".*" ".*"
	set +x
else
	echo "RabbitMQ user admin already exists"
fi

if [ $(echo ${RABBIT_USERS} | grep "\bnode" | wc -l | tr -d " ") -eq 0 ] ; then
	set -x
	docker exec -ti ${container_name} rabbitmqctl add_user node waggle
	docker exec -ti ${container_name} rabbitmqctl set_permissions node "pull-images" ".*" "pull-images"
	set +x
else
	echo "RabbitMQ user node already exists"
fi



if [ $(echo ${RABBIT_USERS} | grep "\bserver" | wc -l | tr -d " ") -eq 0 ] ; then
	set -x
	docker exec -ti ${container_name} rabbitmqctl add_user server waggle
	docker exec -ti ${container_name} rabbitmqctl set_permissions server ".*" ".*" ".*"
	set +x
else
	echo "RabbitMQ user server already exists"
fi



if [ $(echo ${RABBIT_USERS} | grep "\brouter" | wc -l | tr -d " ") -eq 0 ] ; then
	set -x
	docker exec -ti ${container_name} rabbitmqctl add_user router router
	docker exec -ti ${container_name} rabbitmqctl set_permissions router ".*" ".*" ".*"
	set +x
else
	echo "RabbitMQ user router already exists"
fi



if [ $(echo ${RABBIT_USERS} | grep "\bloader_raw" | wc -l | tr -d " ") -eq 0 ] ; then
	set -x
	docker exec -ti ${container_name} rabbitmqctl add_user loader_raw waggle
	docker exec -ti ${container_name} rabbitmqctl set_permissions loader_raw "^db-raw$" "^$" "^db-raw$"
	set +x
else
	echo "RabbitMQ user loader_raw already exists"
fi
