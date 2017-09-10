#!/bin/bash


# This script creates the "server"-certificate for the RabbitMQ server.

set -e
set -x

export SSL_DIR="/usr/lib/waggle/SSL"

cd ${SSL_DIR} # in SSL/

mkdir -p server
chmod 744 server
cd ${SSL_DIR}/server

# Make the server key
openssl genrsa -out key.pem 2048

# create request
openssl req -new -key key.pem -out req.pem -outform PEM \
	-subj /CN=$(hostname)/O=server/ -nodes

cd ${SSL_DIR}/waggleca

# Make the server certificate
openssl ca -config /usr/lib/waggle/beehive-server/SSL/waggleca/openssl.cnf -in ${SSL_DIR}/server/req.pem -out \
	${SSL_DIR}/server/cert.pem -notext -batch -extensions server_ca_extensions

cd ${SSL_DIR}/server

openssl pkcs12 -export -out keycert.p12 -in cert.pem -inkey key.pem -passout pass:waggle

