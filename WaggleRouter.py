# WaggleRouter.py
import sys
sys.path.append("..")
sys.path.append("/usr/lib/waggle/")
from multiprocessing import Process, Manager
from config import *
import pika
from waggle_protocol.protocol.PacketHandler import *
from waggle_protocol.utilities.packetassembler import PacketAssembler
import logging
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class WaggleRouter(Process):
    """
        The WaggleRouter class receives all messages from the incoming queue in the RabbitMQ server.
        It then reads the packet header to learn the message Major type, and forwards it to the appropriate
        queue for processing.
    """
    def __init__(self,routing_table):
        logger.info("Initializing Routing Process")
        logger.debug("debug mode")
        super(WaggleRouter,self).__init__()

        self.routing_table = routing_table

        self.routeQueues    = {
            'r' : 'registration',
            't' : 'util',
            'p' : 'util',
            's' : 'data'
        }
        
        #Connect to rabbitMQ
        try:
            self.rabbitConn = pika.BlockingConnection(pika_params)
        except Exception as e:
            logger.error("Could not connect to RabbitMQ server \"%s\": %s" % (pika_params.host, str(e)))
            sys.exit(1)
    
        logger.info("Connected to RabbitMQ server \"%s\"" % (pika_params.host))
        
        self.channel = self.rabbitConn.channel()
        self.channel.basic_qos(prefetch_count=1)
        # self.assembler = PacketAssembler()

        #Load all of the existing registered node queues
        if os.path.isfile('registrations/nodes.txt'):
            with open('registrations/nodes.txt','r') as nodes:
                for line in nodes:
                    if line and line != '\n':
                        info = line.strip().split(":")
                        self.channel.queue_declare(info[1])

        #declare the default queues
        #TODO: Check to see if this section can be culled.
        queue_list = ["incoming","registration","util"]
        for queueName in queue_list:
            self.channel.queue_declare(queueName)

        #Start consuming things from the incoming queue
        self.channel.basic_consume(self.gotPacket,queue='incoming')


    def gotPacket(self,ch,method,props,body):
        try:
            header = get_header(body)
        except Exception as e:
            logger.error(str(e))
            ch.basic_ack(delivery_tag = method.delivery_tag)
            return
        
        logger.debug("message from %d for %d" % (header['s_uniqid'], header['r_uniqid']) )

        if (header['r_uniqid'] == 0): # If the message is intended for the cloud...

            msg_type = chr(header["msg_mj_type"]),chr(header["msg_mi_type"])
            #Figure out which queue this message belongs in.
            msg_dest = self.routeQueues.get(msg_type[0],'invalid')
            if(msg_dest == 'invalid'):
                ch.basic_ack(delivery_tag = method.delivery_tag)
                return
            self.channel.basic_publish(exchange='internal',routing_key=msg_dest, body=body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        else: # This is a message for someone else. Send it along.
            try:
                #TODO: This is where we have to check if the senderis allowed
                #to send a message to the recipient. We need a permissions system
                #here, with the permissions stored in the Cassandra data base.
                # check if the sender is not impersonating someone else - is that
                #possible? If so, where would that be done? - Check and see if
                #RabbitMq permission system will help (Ben's idea)

                recipient = self.routing_table[header['r_uniqid']]
                self.channel.basic_publish(exchange='internal', routing_key = recipient, body=body)
            except Exception as e:
                print str(e)
            finally:
                ch.basic_ack(delivery_tag =method.delivery_tag)




    def run(self):
        self.channel.start_consuming()

    def join(self):
        super(WaggleRouter,self).terminate()
        self.rabbitConn.close()


