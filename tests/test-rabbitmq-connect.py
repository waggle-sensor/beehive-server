#!/usr/bin/env python3
import pika
import ssl
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('ca_dir')
parser.add_argument('node_dir')
args = parser.parse_args()

ssl_options = {
    'ca_certs': os.path.join(args.ca_dir, 'cacert.pem'),
    'certfile': os.path.join(args.node_dir, 'cert.pem'),
    'keyfile': os.path.join(args.node_dir, 'key.pem'),
    'cert_reqs': ssl.CERT_REQUIRED,
}

connection_parameters = pika.ConnectionParameters(
    host='localhost',
    port=23181,
    credentials=pika.credentials.ExternalCredentials(),
    ssl=True,
    ssl_options=ssl_options)

connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

input('Press any key to close.')

connection.close()
