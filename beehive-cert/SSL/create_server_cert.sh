#!/bin/bash
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license


echo "This script is deprecated. The cert server takes over this functionality."

exit 1



# This script creates the "server"-certificate for the RabbitMQ server.

set -e


# TODO Cleanup this script and have it not destroy existing info.

export SSL_DIR="/usr/lib/waggle/SSL"

if [ -z "$1" ]; then
	commonname="rabbitmq"
else
	commonname="$1"
fi

set -x

cd ${SSL_DIR} # in SSL/

mkdir -p server
chmod 755 server
cd ${SSL_DIR}/server

if [ -e key.pem ] ; then
 echo "key.pem already exists, skipping..."
 exit 0
fi


# Make the server key
openssl genrsa -out key.pem 2048

# create random seed file
openssl rand -out ${SSL_DIR}/server/random.rnd 20
ln -sf ${SSL_DIR}/server/random.rnd /root/.rnd


# create request
openssl req -rand ${SSL_DIR}/server/random.rnd -new -key key.pem -out req.pem -outform PEM \
	-subj /CN=$commonname/O=server/ -nodes

sleep 1

if [ ! -f ${SSL_DIR}/server/req.pem ] ; then
	echo "File missing: ${SSL_DIR}/server/req.pem "
	exit 1
fi


cd ${SSL_DIR}/waggleca

# Make the server certificate
openssl ca -config openssl.cnf -in ${SSL_DIR}/server/req.pem -out \
	${SSL_DIR}/server/cert.pem -notext -batch -extensions server_ca_extensions

cd ${SSL_DIR}/server

openssl pkcs12 -export -out keycert.p12 -in cert.pem -inkey key.pem -passout pass:waggle
