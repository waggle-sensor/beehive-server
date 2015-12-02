#!/bin/bash


export SSL_DIR="/usr/lib/waggle/SSL"

# Begin constructing the Certificate Authority

mkdir -p /usr/lib/waggle
chmod 777 -R /usr/lib/waggle


rm -rf ${SSL_DIR}/waggleca
mkdir -p ${SSL_DIR}/waggleca

cd ${SSL_DIR}/waggleca

# Make appropriate folders
mkdir -p certs private
chmod 700 private
echo 01 > serial
touch index.txt

# Generate the root certificate

openssl req -x509 -config /usr/lib/waggle/beehive-server/SSL/waggleca/openssl.cnf -newkey rsa:2048 -days 365 \
	-out cacert.pem -outform PEM -subj /CN=waggleca/ -nodes

openssl x509 -in cacert.pem -out cacert.cer -outform DER


