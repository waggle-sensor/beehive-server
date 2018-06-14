#!/bin/bash

SSL_DIR="/usr/lib/waggle/SSL"
CA_DIR="${SSL_DIR}/waggleca"

mkdir -p $CA_DIR
#chmod 700 $SSL_DIR
chmod 700 $CA_DIR

cd $CA_DIR

# Make appropriate folders
mkdir certs private
chmod 700 private

if [ ! -f serial ]; then
	echo 01 > serial
fi

touch index.txt

# this is needed for "node" certificates. We may change that later.
echo "unique_subject = no" > index.txt.attr

# Generate the root certificate

if [ -f "$CA_DIR/private/cakey.pem" ]; then
	echo "Error: CA key already exists."
fi

if [ -f "$CA_DIR/cacert.pem" ]; then
	echo "Error: CA cert already exists."
fi

openssl req \
	-x509 \
	-config /usr/lib/waggle/beehive-server/beehive-cert/SSL/waggleca \
	-newkey rsa:2048 \
	-keyform PEM \
	-nodes \
	-days 365 \
	-out cacert.pem \
	-outform PEM \
	-subj /CN=waggleca/

openssl x509 -in cacert.pem -out cacert.cer -outform DER
