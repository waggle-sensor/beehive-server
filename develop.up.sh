#!/bin/bash -e

docker-compose -f docker-compose.develop.yml up -d --build

echo "configuring cassandra"

while ! docker-compose -f docker-compose.develop.yml exec -T beehive-cassandra cqlsh < beehive-cassandra/init.cql; do
    echo "waiting for cassandra..."
    sleep 3
done

echo "configuring cert server"

while ! docker-compose -f docker-compose.develop.yml exec beehive-cert true; do
    echo "waiting for cert server..."
    sleep 3
done

docker-compose -f docker-compose.develop.yml exec beehive-cert SSL/create_certificate_authority.sh
docker-compose -f docker-compose.develop.yml exec beehive-cert SSL/create_server_cert.sh
