import os.path
import pika
import ssl
from urllib.parse import urlencode


url = 'amqps://node:waggle@beehive1.mcs.anl.gov:23181?{}'.format(urlencode({
    'ssl': 't',
    'ssl_options': {
        'certfile': os.path.abspath('SSL/node/cert.pem'),
        'keyfile': os.path.abspath('SSL/node/key.pem'),
        'ca_certs': os.path.abspath('SSL/waggleca/cacert.pem'),
        'cert_reqs': ssl.CERT_REQUIRED
    }
}))

# this should all get abstracted out

connection = pika.BlockingConnection(pika.URLParameters(url))

channel = connection.channel()

channel.exchange_declare(exchange='plugins.in', exchange_type='direct')
channel.exchange_bind(source='data-pipeline-in', destination='plugins.in')

channel.queue_declare(queue='example:1', durable=True)
channel.queue_bind(queue='example:1', exchange='plugins.in', routing_key='example:1')


def callback(ch, method, properties, body):
    print(properties.reply_to)
    print(properties.timestamp)
    print(properties.type)
    print(body)
    print()


channel.basic_consume(callback,
                      queue='example:1',
                      no_ack=True)

channel.start_consuming()
