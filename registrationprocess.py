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
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RegProcess(Process):
    """
        This process handles all registration requests.
        It is responsible to receiving all requests, updating the routing table,
        and writing the routing information to a permanent file.
    """
    def __init__(self,node_table):
        """
            Starts up the Registration Process
        """
        super(RegProcess,self).__init__()
        self.node_table = node_table
        self.session = None
        self.cluster = None
        self.connection = None
        
        logger.info("Initializing RegProcess")

        self.cassandra_init()
        # Set up the Rabbit connection
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        while True:
            try:
                self.connection = pika.BlockingConnection(pika_params)
            except Exception as e:
                logger.error("Could not connect to RabbitMQ server \"%s\": %s" % (pika_params.host, e))
                time.sleep(1)
                continue
            break
       
        
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
        
        header,msg = unpack(body)
        s_uniqid_str = nodeid_int2hexstr(header["s_uniqid"])
        
        major = chr(header["msg_mj_type"])
        minor = chr(header["msg_mi_type"])
        
        logger.info("Received a registration request (%s%s) from node \"%s\"." % (major, minor, s_uniqid_str))
        
        # Unpack the header and see if it is already registered
        
        minor_type = None
        # while is not used as a loop, I just want to use break
        while True:
            if minor == 'r':
            
                #
                #  DEPRECATED for now. (major, minor = rr)
                #
                logger.error("rr is deprecated")
                break
            
                if header["s_uniqid"] in self.node_table:
                    minor_type = ord('a');
                else:
                    logger.info("Registering new node.")
                    # Add the node to the registration file and make and bind its queue
                    #if not os.path.exists('registrations'):
                    #    os.makedirs('registrations')
                    #with open('registrations/nodes.txt','a+') as nodeList:
                    #    nodeList.write("{}:{}\n".format(str(header["s_uniqid"]),msg))
                
                    s_uniqid_int = header["s_uniqid"]
                
                    self.cassandra_register_node()
                
                
                    self.channel.queue_declare(msg)
                    self.channel.queue_bind(exchange='internal',queue=msg,routing_key=msg)
                    #self.routing_table[header["s_uniqid"]] = msg
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

            elif minor == 's': # They want to get an SSL Certificate
        
                #
                # DEPRECATED
                #
                logger.error("Someone wants an SSL cert.")
                break
            
            
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

            elif minor == 'n': # They are sending us a config file.
            # Cassandra note: If the node is already in the node_info table,
            # then this will preform an UPSERT of the config file instead of an INSERT.
            # This is inherent to Cassandra, so is not explicitly stated here.
        
                # convert int to hex_str
                config_dict = {}
                try:
                    config_dict = json.loads(msg)
                except ValueError, e:
                    logger.error("error parsing json (msg=%s): %s" % (msg, str(e)))
                    break
        
                node_id = config_dict['node_id']
            
                if s_uniqid_str != node_id:
                    logger.error("Sender node IDs do not match. header=%s config=%s" % (s_uniqid_str, node_id) )
                    break
            
                logger.info("registration request from node %s" % (node_id))
                queue = config_dict['queue']
                self.channel.queue_declare(queue)
                self.channel.queue_bind(exchange='internal',queue=msg,routing_key=queue)
            
                node_name = config_dict['name']
                if not node_name:
                    node_name = "unknown"
            
                try:
                    #self.cassandra_insert(header,msg)
                    self.cassandra_register_node(node_id, queue, node_name)
                except Exception as e:
                    logger.warning("Cassandra connection failed. Will retry soon... "+ str(e))
                    time.sleep(1)
                    self.cassandra_connect()
                    break
                
                # update node_table
                node_table[node_id] = {'queue' : queue , 'name' : node_name}
            
                # Send the node a registration confirmation.
                resp_header = {
                        "msg_mj_type" : ord('r'),
                        "msg_mi_type" : ord('n'),
                        "r_uniqid"    : header["s_uniqid"],
                        "resp_session": header["snd_session"]
                }
                msg = "Congratulations node {}! You are registered under the queue {}!".format(s_uniqid_str, queue)
                for packet in pack(resp_header,msg):
                    response = packet
                self.channel.basic_publish(exchange='waggle_in',routing_key="in",body=response)
            break
            
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

    def cassandra_register_node(self, node_id, queue, name):
        
        statement = "INSERT INTO nodes (node_id, timestamp, queue, name) VALUES ('%s', '%s', '%s', '%s')" % (node_id, unix_time_millis(datetime.datetime.now()), queue, name)
        
        
        while True:
            self.cassandra_connect()
            success = True
            
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


        sensor_data_cql = '''CREATE TABLE IF NOT EXISTS waggle.sensor_data (
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
        
        
        
        statements = [keyspace_cql, sensor_data_cql, nodes_cql]
        
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
