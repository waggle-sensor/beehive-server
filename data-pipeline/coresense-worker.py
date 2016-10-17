import os.path
import pika
import ssl
from waggle.coresense.utils import decode_frame
from urllib.parse import urlencode
import json


plugin = 'coresense:3'

url = 'amqps://node:waggle@beehive1.mcs.anl.gov:23181?{}'.format(urlencode({
    'ssl': 't',
    'ssl_options': {
        'certfile': os.path.abspath('SSL/node/cert.pem'),
        'keyfile': os.path.abspath('SSL/node/key.pem'),
        'ca_certs': os.path.abspath('SSL/waggleca/cacert.pem'),
        'cert_reqs': ssl.CERT_REQUIRED
    }
}))

connection = pika.BlockingConnection(pika.URLParameters(url))

channel = connection.channel()

channel.exchange_declare(exchange='plugins-in',
                         exchange_type='direct')

channel.exchange_bind(source='data-pipeline-in',
                      destination='plugins-in')

channel.queue_declare(queue=plugin,
                      durable=True)

channel.queue_bind(queue=plugin,
                   exchange='plugins-in',
                   routing_key=plugin)

channel.exchange_declare(exchange='plugins-out',
                         exchange_type='fanout',
                         durable=True)


def callback(ch, method, properties, body):
    for sensor, values in decode_frame(body).items():
        props = pika.BasicProperties(
            app_id=properties.app_id,
            timestamp=properties.timestamp,
            reply_to=properties.reply_to,
            type=sensor,
            content_type='text/json',
        )

        channel.basic_publish(properties=props,
                              exchange='plugins-out',
                              routing_key=method.routing_key,
                              body=json.dumps(values))


channel.basic_consume(callback,
                      queue=plugin,
                      no_ack=True)

channel.start_consuming()
