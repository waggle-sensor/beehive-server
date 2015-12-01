#!/bin/bash


# this script creates the client-certificates for the RabbitMQ server.
# This is used for nodes and the beehive-server.

export SSL_DIR="/usr/lib/waggle/SSL"

if [ ! $# -eq 2 ];  then
    echo "usage: ./create_client_cert.sh node|server <dirname>"
    echo " example: ./create_client_cert.sh node node1"
fi

RABBIT_USER=$1

# refers to beehive-sever, not RabbitMQ.
if [ "${RABBIT_USER}_" != "node" ] && [ "${RABBIT_USER}_" == "server" ] ; then
  echo 'error: first argument must be either "node" or "server"'
  exit 1
fi


export CERT_DIR=$2



rm -rf ${SSL_DIR}/${CERT_DIR}
mkdir -p ${SSL_DIR}/${CERT_DIR}


# create key
cd ${SSL_DIR}/${CERT_DIR}
openssl genrsa -out key.pem 2048

# create certificate request
openssl req -new -key ./key.pem -out req.pem -outform PEM \
    -subj /CN=${RABBIT_USER}/O=client/ -nodes

cd ${SSL_DIR}/waggleca

# sign
openssl ca -config ${SSL_DIR}/waggleca/openssl.cnf -in ${SSL_DIR}/${CERT_DIR}/req.pem -out  ${SSL_DIR}/${CERT_DIR}/cert.pem -notext -batch -extensions client_ca_extensions

# pkcs12 , might be needed for java clients for example. Not sure if we actually need that.
openssl pkcs12 -export -out ${SSL_DIR}/${CERT_DIR}/keycert.p12 -in ${SSL_DIR}/${CERT_DIR}/cert.pem -inkey ${SSL_DIR}/${CERT_DIR}/key.pem -passout pass:waggle