
#!bin/bash

set -e
#set -x


if [ $# -lt 1 ]; then
  echo 1>&2 "$0: not enough arguments"
  exit 2
elif [ $# -gt 1 ]; then
  echo 1>&2 "$0: too many arguments"
  exit 2
fi


if [ -z ${RABBITMQ_ADMIN_PASSWORD} ] ; then
	echo "Varibale RABBITMQ_ADMIN_PASSWORD not set"
	exit 1
fi


#echo "RABBITMQ_ADMIN_PASSWORD: ${RABBITMQ_ADMIN_PASSWORD}"

container_name=${1}

echo name=${name}

# wait for rabbitmq to up
docker exec -ti ${container_name} rabbitmqctl status > /dev/null


RABBIT_USERS=$( for i in $(docker exec -ti ${container_name} rabbitmqctl list_users -q) ; do echo $i  ; done | grep -v "^\[" )

# \b is matches word boundary

if [ $(echo ${RABBIT_USERS} | grep "\badmin" | wc -l | tr -d " ") -eq 0 ] ; then
	set -x
	docker exec -ti ${container_name} rabbitmqctl add_user admin ${RABBITMQ_ADMIN_PASSWORD}
	docker exec -ti ${container_name} rabbitmqctl set_user_tags admin administrator
	docker exec -ti ${container_name} rabbitmqctl set_permissions admin ".*" ".*" ".*"
	set +x
fi

if [ $(echo ${RABBIT_USERS} | grep "\bnode" | wc -l | tr -d " ") -eq 0 ] ; then
	set -x
	docker exec -ti ${container_name} rabbitmqctl add_user node waggle
	docker exec -ti ${container_name} rabbitmqctl set_permissions node "pull-images" ".*" "pull-images"
	set +x
fi



if [ $(echo ${RABBIT_USERS} | grep "\bserver" | wc -l | tr -d " ") -eq 0 ] ; then
	set -x
	docker exec -ti ${container_name} rabbitmqctl add_user server waggle
	docker exec -ti ${container_name} rabbitmqctl set_permissions server ".*" ".*" ".*"
	set +x
fi



if [ $(echo ${RABBIT_USERS} | grep "\brouter" | wc -l | tr -d " ") -eq 0 ] ; then
	set -x
	docker exec -ti ${container_name} rabbitmqctl add_user router router
	docker exec -ti ${container_name} rabbitmqctl set_permissions router ".*" ".*" ".*"
	set +x
fi



if [ $(echo ${RABBIT_USERS} | grep "\bloader_raw" | wc -l | tr -d " ") -eq 0 ] ; then
	set -x
	docker exec -ti ${container_name} rabbitmqctl add_user loader_raw waggle
	docker exec -ti ${container_name} rabbitmqctl set_permissions loader_raw "^db-raw$" "^$" "^db-raw$"
	set +x
fi
