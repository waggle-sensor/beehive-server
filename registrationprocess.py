# registrationprocess.py
import sys
import os
sys.path.append("..")
sys.path.append("/usr/lib/waggle/")
from multiprocessing import Process, Manager
from config import *
import pika
from waggle_protocol.protocol.PacketHandler import *
import logging
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)
from crcmod.predefined import mkCrcFun
from cassandra.cluster import Cluster
import time


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RegProcess(Process):
    """
        This process handles all registration requests.
        It is responsible to receiving all requests, updating the routing table,
        and writing the routing information to a permanent file.
    """
    def __init__(self,routing_table):
        """
            Starts up the Registration Process
        """
        super(RegProcess,self).__init__()
        self.routing_table = routing_table
        self.session = None
        self.cluster = None
        
        logger.info("Initializing RegProcess")

        self.cassandra_init()
        # Set up the Rabbit connection
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        try:
            self.connection = pika.BlockingConnection(pika_params)
        except Exception as e:
            logger.error("Could not connect to RabbitMQ server \"%s\": %s" % (pika_params.host, e))
            sys.exit(1)
    
        
       
        
        logger.info("Connected to RabbitMQ server \"%s\"" % (pika_params.host))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        # Declare this process's queue
        self.channel.queue_declare("registration")
        try:
            self.channel.basic_consume(self.callback, queue='registration')
        except Exception as e:
            logger.warning("channel.basic_consume crashed :"+ str(e))
        

    def callback(self,ch,method,props,body):
        """
            Handles incoming registration messages, including:
                Initial registration (subtype 'r')
                SSL Certificate Registration (subtype 's')
                Configuration file registration (subtype 'n')

            Each subtype is handled as a apart of an if-elif statement.
        """
        logger.info("Received a registration request.")

        # Unpack the header and see if it is already registered
        header,msg = unpack(body)
        minor_type = None
        if header["msg_mi_type"] == ord('r'):
            if header["s_uniqid"] in self.routing_table:
                minor_type = ord('a');
            else:
                logger.info("Registering new node.")
                # Add the node to the registration file and make and bind its queue
                if not os.path.exists('registrations'):
                    os.makedirs('registrations')
                with open('registrations/nodes.txt','a+') as nodeList:
                    nodeList.write("{}:{}\n".format(str(header["s_uniqid"]),msg))
                self.channel.queue_declare(msg)
                self.channel.queue_bind(exchange='internal',queue=msg,routing_key=msg)
                self.routing_table[header["s_uniqid"]] = msg
                minor_type = ord('n')

            # Send the node a registration confirmation.
            resp_header = {
                    "msg_mj_type" : ord('r'),
                    "msg_mi_type" : minor_type,
                    "r_uniqid"    : header["s_uniqid"],
                    "resp_session": header["snd_session"]
            }
            msg = "Congratulations node {}! You are registered under the queue {}!".format(header["s_uniqid"],msg)
            for packet in pack(resp_header,msg):
                response = packet
            self.channel.basic_publish(exchange='waggle_in',routing_key="in",body=response)

        elif header["msg_mi_type"] == ord('s'): # They want to get an SSL Certificate
            logger.info("Someone wants an SSL cert.")
            # Write the request to a file to be used by the CA for signing
            replyQueue = msg.split("\n")[0]
            msg = "\n".join(msg.split("\n")[1:])
            print replyQueue
            certFile = "/tmp/" + self.name
            with open(certFile + "_req.pem","w+") as cert:
                cert.write(msg)
            cmd = "openssl ca -config /usr/lib/waggle/SSL/waggleca/openssl.cnf " + \
                "-in " + certFile + "_req.pem" + " -out " + certFile + "_cert.pem " + \
                "-notext -batch -extensions client_ca_extensions"
            os.system(cmd)
            cert = ""
            with open(certFile + "_cert.pem","r") as cert:
            	cert = cert.read()
            	print cert
            ch.basic_publish(exchange='',
                 routing_key=replyQueue,
                 body=cert)

        elif header["msg_mi_type"] == ord('n'): # They are sending us a config file.
        # Cassandra note: If the node is already in the node_info table,
        # then this will preform an UPSERT of the config file instead of an INSERT.
        # This is inherent to Cassandra, so is not explicitly stated here.
            try:
                self.cassandra_insert(header,msg)
            except Exception as e:
                logger.warning("Cassandra connection failed. Will retry soon... "+ str(e))
                ch.basic_nack(delivery_tag = method.delivery_tag)
                time.sleep(1)
                self.cassandra_connect()
                return


        ch.basic_ack(delivery_tag = method.delivery_tag)

    def cassandra_insert(self,header,data):
        """
            Insert a list of data into the currently connected Cassandra database.
        """
        
        if self.session == None:
            self.cassandra_connect()
        
        try:
            prepared_statement = self.session.prepare("INSERT INTO node_info" + \
                " (node_id, timestamp, config_file)" + \
                " VALUES (?, ?, ?)")
        except Exception as e:
            logger.error("self.session.prepare crashed: "+str(e))
            raise
            
        # convert int to hex_str
        s_uniqid_str = nodeid_int2hexstr(header["s_uniqid"])
        try:            
            #bound_statement = prepared_statement.bind([header["s_uniqid"],time.time()*1000,data])
            bound_statement = prepared_statement.bind([s_uniqid_str,time.time()*1000,data])
        except Exception as e:
            logger.error("prepared_statement.bind: "+str(e))
            raise
        try:        
            self.session.execute(bound_statement)
        except Exception as e:
            logger.error("self.session.execute crashed: "+str(e))
            raise


    def cassandra_connect(self):
        """
            Try to establish a new connection to Cassandra.
        """
        
        
        while self.session == None:     
            try:
                self.cluster.shutdown()
            except:
                pass
            
            try:    
                self.cluster = Cluster(contact_points=[CASSANDRA_HOST])
            except Exception as e:
                logger.error("self.cluster.connect failed: " + str(e))
                time.sleep(1)
                continue
                
            try: # Might not immediately connect. That's fine. It'll try again if/when it needs to.
                self.session = self.cluster.connect('waggle')
            except Exception as e:
                logger.error("(self.cluster.connect): Cassandra connection to " + CASSANDRA_HOST + " failed: " + str(e))
                time.sleep(3)
                continue
            
    def cassandra_init(self):
        
        
        keyspace_cql = '''CREATE KEYSPACE IF NOT EXISTS waggle WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '2'}  AND durable_writes = true;'''


        sensor_data_cql = '''CREATE TABLE waggle.sensor_data (
                                node_id ascii,
                                sensor_name ascii,
                                timestamp timestamp,
                                data list<double>,
                                data_types list<ascii>,
                                extra_info list<ascii>,
                                units list<ascii>,
                                PRIMARY KEY (node_id, sensor_name, timestamp)
                            );'''
        sensor_data_cql = sensor_data_cql.replace('\n', ' ').replace('\r', '')

        node_info_cql = '''CREATE TABLE waggle.node_info (
                            node_id ascii PRIMARY KEY,
                            timestamp timestamp,
                            config_file ascii,
                            extra_notes list<ascii>,
                            sensor_names list<ascii>,
                            height double,
                            latitude double,
                            longitude double,
                            name ascii
                        );'''
        node_info_cql = node_info_cql.replace('\n', ' ').replace('\r', '')
        
            
        node_table_cql = '''CREATE TABLE waggle.nodes (
                        node_id ascii,
                        queue ascii,
                        extension_nodes list<ascii>,
                        updated timestamp,
                        PRIMARY KEY (node_id)
                        );'''
        node_table_cql = node_table_cql.replace('\n', ' ').replace('\r', '')
        
        
        statements = [keyspace_cql, sensor_data_cql, node_info_cql, node_table_cql]
        
        while True:
            self.cassandra_connect()
            success = True
            for statement in statements:
                try: 
                    self.session.execute(statement)
                except Exception as e:
                    logger.error("(self.session.execute(statement)) failed. Statement: %s Error: %s " % (statement, str(e)) )
                    success = False
                    break
                    
            if success:
                break
            else:
                time.sleep(5)
          
        logger.debug("Cassandra database initialized.")


    def run(self):
        self.cassandra_connect()
        self.channel.start_consuming()


    def join(self):
        super(RegProcess,self).terminate()
        self.connection.close()
