#!/bin/bash
set -e

# this script creates the client-certificates for the RabbitMQ server.
# This is used for nodes and the beehive-server.

export SSL_DIR="/usr/lib/waggle/SSL"

if [ ! $# -eq 2 ];  then
    echo "usage: ./create_client_cert.sh node|server <dirname>"
    echo " example: ./create_client_cert.sh node node1"
    exit 1
fi

RABBIT_USER=$1

# refers to beehive-sever, not RabbitMQ.
if [ "${RABBIT_USER}_" != "node_" ] && [ "${RABBIT_USER}_" != "server_" ] ; then
  echo 'error: first argument must be either "node" or "server"'
  exit 1
fi


export CERT_DIR=$2

set -x

rm -rf ${SSL_DIR}/${CERT_DIR}
mkdir -p ${SSL_DIR}/${CERT_DIR}


# create key
cd ${SSL_DIR}/${CERT_DIR}
openssl genrsa -out key.pem 2048

chmod 600 key.pem

# create public RSA to allow node to create reverse ssh tunnel
# -y          : Read private key file and print public key.
# -f filename : Filename of the key file.
ssh-keygen -y -f key.pem > key_rsa.pub.tmp
mv key_rsa.pub.tmp key_rsa.pub

# create certificate request
openssl req -new -key ./key.pem -out req.pem -outform PEM \
    -subj /CN=${RABBIT_USER}/O=client/ -nodes

cd ${SSL_DIR}/waggleca

# sign
openssl ca -config openssl.cnf -in ${SSL_DIR}/${CERT_DIR}/req.pem -out  ${SSL_DIR}/${CERT_DIR}/cert.pem -notext -batch -extensions client_ca_extensions

# pkcs12 , might be needed for java clients for example. Not sure if we actually need that.
openssl pkcs12 -export -out ${SSL_DIR}/${CERT_DIR}/keycert.p12 -in ${SSL_DIR}/${CERT_DIR}/cert.pem -inkey ${SSL_DIR}/${CERT_DIR}/key.pem -passout pass:waggle
