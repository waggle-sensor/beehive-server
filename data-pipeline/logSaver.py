#!/usr/bin/env python3
import argparse
import datetime
import multiprocessing
import pika
import time

class LogSaverProcess(multiprocessing.Process):
    def __init__(self, q, verbosity = 0):
        super(LogSaverProcess, self).__init__()
        self.q = q
        self.verbosity = verbosity
        
        # set up the rabbitmq connection
        self.credentials = pika.PlainCredentials('log_saver', 'waggle')
        self.parameters = pika.ConnectionParameters('beehive-rabbitmq', credentials = self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue='log-saver', durable=True)
        self.channel.queue_bind(queue='log-saver', exchange='logs', routing_key='#')

        self.channel.basic_consume(self.callback, queue='log-saver', no_ack=False)

    def callback(self, ch, method, properties, body):
        try:
            node_id = properties.reply_to.lower()
            headers = properties.headers
            priority = headers['value']
            strUtcNow = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            s = '{} <{}> {} {}'.format(strUtcNow, priority, node_id, body.decode())
            print(s, flush=True)

            if self.verbosity > 3:
                print(' ch = {}'.format(repr(ch)))
                print(' method = {}'.format(repr(method)))
                print(' properties  = {}'.format(repr(properties)))
                print(' body   = {}'.format(repr(body)))
            
            self.q.put((node_id, s), block = False)
            if self.verbosity > 1: print('  caching:  ', node_id,  'self.q.qsize() = ', self.q.qsize())
        except Exception as e:
            print("Error inserting (queue size = %d)  data = %s" % (self.q.qsize(), str(e)))
            print(' method = {}'.format(repr(method)))
            print(' properties  = {}'.format(repr(properties)))
            print(' body   = {}'.format(repr(body)))
            ch.basic_ack(delivery_tag = method.delivery_tag)
            return

        ch.basic_ack(delivery_tag = method.delivery_tag)

    def run(self):
        self.channel.start_consuming()

    def join(self):
        super(LogSaverProcess, self).terminate()
        self.connection.close(0)

#_______________________________________________________________________
if __name__ == '__main__':

    # command-line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--verbose', '-v', action = 'count')
    argParser.add_argument('-debug', action = 'store_true')
    args = argParser.parse_args()
    verbosity = 0 if not args.verbose else args.verbose
    if verbosity: print('args =', args)

    q = multiprocessing.Queue(1000)
    p = LogSaverProcess(q, verbosity)
    p.start()

    print(__name__ + ': created process ', p)
    time.sleep(3)
    
    while p.is_alive():
        # stage 1 - empty queue to dictionary of lists - one list of strings per node_id
        d = {}
        for _i in range(3):
            while not q.empty():
                data = q.get()
                node_id = data[0]
                s = data[1]
                if node_id not in d:
                    d[node_id] = [s]
                else:
                    d[node_id].append(s)
                    if verbosity: print('   {}  has  {} '.format(node_id, len(d[node_id])))
            time.sleep(1)
        
        # stage 2 - periodically write all strings to the appropriate files, batched by node_id
        for node_id in d:
            filename = '/mnt/beehive/node-logs/{}'.format(node_id)
            with open(filename, 'a+') as f:
                for s in d[node_id]:
                    f.write(s.strip() + '\n')
        d.clear() # free the memory
    print(__name__ + ': process is dead, time to die')
    p.join()    
