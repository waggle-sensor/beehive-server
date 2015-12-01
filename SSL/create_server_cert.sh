#!/bin/bash


export SSL_DIR="/usr/lib/waggle/SSL"


# Make the server certificate

cd ${SSL_DIR} # in SSL/

mkdir -p server
chmod 744 server
cd ${SSL_DIR}/server

openssl genrsa -out key.pem 2048

openssl req -new -key key.pem -out req.pem -outform PEM \
	-subj /CN=server/O=server/ -nodes

cd ${SSL_DIR}/waggleca

openssl ca -config openssl.cnf -in ${SSL_DIR}/server/req.pem -out \
	${SSL_DIR}/server/cert.pem -notext -batch -extensions server_ca_extensions

cd ${SSL_DIR}/server

openssl pkcs12 -export -out keycert.p12 -in cert.pem -inkey key.pem -passout pass:waggle

