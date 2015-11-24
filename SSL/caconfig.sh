#!/bin/bash


./create_certificate_authority.sh

./create_server_cert.sh

# Copy files to correct places
cp /usr/lib/waggle/SSL/rabbitmq.config /etc/rabbitmq/

