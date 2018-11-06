#!/bin/bash


# This script creates the "server"-certificate for the RabbitMQ server.

set -e
set -x

# TODO Cleanup this script and have it not destroy existing info.

export SSL_DIR="/usr/lib/waggle/SSL"

if [ -z "$1" ]; then
	commonname="rabbitmq"
else
	commonname="$1"
fi

cd ${SSL_DIR} # in SSL/

mkdir -p server
chmod 755 server
cd ${SSL_DIR}/server

# Make the server key
openssl genrsa -out key.pem 2048

# create request
openssl req -new -key key.pem -out req.pem -outform PEM \
	-subj /CN=$commonname/O=server/ -nodes

cd ${SSL_DIR}/waggleca

# Make the server certificate
openssl ca -config openssl.cnf -in ${SSL_DIR}/server/req.pem -out \
	${SSL_DIR}/server/cert.pem -notext -batch -extensions server_ca_extensions

cd ${SSL_DIR}/server

openssl pkcs12 -export -out keycert.p12 -in cert.pem -inkey key.pem -passout pass:waggle
