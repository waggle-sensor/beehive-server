#!/usr/bin/env python

import sys, os, StringIO, ConfigParser, logging, pika, ssl
import time, datetime


CONFIG_FILE="/etc/waggle/beehive-server.cfg"

loglevel=logging.DEBUG
LOG_FILENAME="/var/log/waggle/communicator/beehive-server.log"
LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - line=%(lineno)d - %(message)s'


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



root_logger = logging.getLogger()
root_logger.setLevel(loglevel)
formatter = logging.Formatter(LOG_FORMAT)

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)

root_logger.handlers = []
root_logger.addHandler(handler)

# log rotate will be activated in main method 

def read_file( str ):
    if not os.path.isfile(str) :
        return ""
    with open(str,'r') as file_:
        return file_.read().strip()
    return ""
    
    

def read_value(key, defaultval):
    value=None
    try:
        value=my_config.get("root", key)
    except ConfigParser.NoOptionError:
        value=""
    
    if not value:
        return defaultval
    
    return value
    
    


ini_str = '[root]\n'
if os.path.isfile(CONFIG_FILE):
    ini_str = ini_str + open(CONFIG_FILE, 'r').read()
    
ini_fp = StringIO.StringIO(ini_str)
my_config = ConfigParser.RawConfigParser()
my_config.readfp(ini_fp)

RABBITMQ_HOST=read_value("rabbitmq-host", "rabbitmq")
logger.info("RABBITMQ_HOST: %s" %(RABBITMQ_HOST))

CASSANDRA_HOST=read_value("cassandra-host", "cassandra")
logger.info("CASSANDRA_HOST: %s" %(CASSANDRA_HOST))



USE_SSL=True
RABBITMQ_PORT=5671


# Beehive server has needs client certificates for RabbitMQ
CLIENT_KEY_FILE="/usr/lib/waggle/SSL/beehive-server/key.pem"
CLIENT_CERT_FILE="/usr/lib/waggle/SSL/beehive-server/cert.pem"

CA_ROOT_FILE="/usr/lib/waggle/SSL/waggleca/cacert.pem"


pika_credentials = pika.PlainCredentials('server', 'waggle')
    
pika_params=pika.ConnectionParameters(  host=RABBITMQ_HOST, 
                                        credentials=pika_credentials, 
                                        virtual_host='/', 
                                        port=RABBITMQ_PORT, 
                                        ssl=USE_SSL, 
                                        ssl_options={"ca_certs": CA_ROOT_FILE , 'certfile': CLIENT_CERT_FILE, 'keyfile': CLIENT_KEY_FILE, 'cert_reqs' : ssl.CERT_REQUIRED} 
                                         )


# cassandra
keyspace_cql = '''CREATE KEYSPACE IF NOT EXISTS waggle WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '2'}  AND durable_writes = true;'''
nodes_cql = '''CREATE TABLE IF NOT EXISTS waggle.nodes (
                    node_id ascii PRIMARY KEY,
                    timestamp timestamp,
                    queue ascii,
                    config_file ascii,
                    extra_notes list<ascii>,
                    sensor_names list<ascii>,
                    height double,
                    latitude double,
                    longitude double,
                    name ascii
                );'''
nodes_cql = nodes_cql.replace('\n', ' ').replace('\r', '')

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return long(unix_time(dt) * 1000.0)
    
    
    
    
    
