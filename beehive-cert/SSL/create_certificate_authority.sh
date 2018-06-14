#!/bin/bash

SSL_DIR="/usr/lib/waggle/SSL"
CA_DIR="${SSL_DIR}/waggleca"

mkdir -p $CA_DIR
#chmod 700 $SSL_DIR
chmod 700 $CA_DIR

cd $CA_DIR

# Make appropriate folders
mkdir -p certs private
chmod 700 private

if [ ! -f serial ]; then
	echo 01 > serial
fi

touch index.txt

# this is needed for "node" certificates. We may change that later.
echo "unique_subject = no" > index.txt.attr

# Generate the root certificate

if [ -f "$CA_DIR/private/cakey.pem" ]; then
	echo "CA key already exists. Will use pre-existing key."
else
	openssl genrsa -out $CA_DIR/private/cakey.pem 2048
	rm $CA_DIR/cacert.pem
fi

if [ -f "$CA_DIR/cacert.pem" ]; then
	echo "Error: CA cert already exists."
else
	openssl req \
		-new \
		-x509 \
		-config /usr/lib/waggle/beehive-server/beehive-cert/SSL/waggleca \
		-key $CA_DIR/private/cakey.pem \
		-days 3650 \
		-out cacert.pem \
		-outform PEM \
		-subj /CN=waggleca/

	# openssl x509 -in cacert.pem -out cacert.cer -outform DER
fi
