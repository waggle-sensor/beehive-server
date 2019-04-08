#!/bin/bash
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
set -e

# this script creates the client-certificates for the RabbitMQ server.
# This is used for nodes and the beehive-server.

export SSL_DIR="/usr/lib/waggle/SSL"

if [ ! $# -eq 2 ];  then
    echo "usage: ./create_client_cert.sh commonname <dirname>"
    echo " example: ./create_client_cert.sh node123 node123"
    exit 1
fi

RABBIT_USER=$1
export CERT_DIR=$2

set -x

mkdir -p ${SSL_DIR}/${CERT_DIR}

cd ${SSL_DIR}/${CERT_DIR}

if [ -f "key.pem" ]; then
  echo "Client private key already exists."
else
  echo "Creating client private key."
  openssl genrsa -out key.pem 2048
  chmod 600 key.pem

  # extract public key from private key
  ssh-keygen -y -f key.pem > key_rsa.pub
fi

if [ -f "cert.pem" ]; then
  echo "Client certificate already exists."
else
  echo "Creating client certificate."
  # create certificate request
  openssl req -new -key ./key.pem -out req.pem -outform PEM \
      -subj "/O=client/CN=${RABBIT_USER}" -nodes

  cd ${SSL_DIR}/waggleca

  # sign
  openssl ca -config openssl.cnf -in ${SSL_DIR}/${CERT_DIR}/req.pem -out  ${SSL_DIR}/${CERT_DIR}/cert.pem -notext -batch -extensions client_ca_extensions

  # pkcs12 , might be needed for java clients for example. Not sure if we actually need that.
  openssl pkcs12 -export -out ${SSL_DIR}/${CERT_DIR}/keycert.p12 -in ${SSL_DIR}/${CERT_DIR}/cert.pem -inkey ${SSL_DIR}/${CERT_DIR}/key.pem -passout pass:waggle
fi
