#!/bin/bash


./SSL/create_certificate_authority.sh

./SSL/create_server_cert.sh

# Copy files to correct places
cp ${SSL_DIR}/rabbitmq.config /etc/rabbitmq/

