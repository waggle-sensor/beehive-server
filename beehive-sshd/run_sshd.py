#!/usr/bin/python

import subprocess
import sys
import select
import time
import MySQLdb

log_forward_prefix = 'debug1: Local forwarding listening on 127.0.0.1 port '

def handle_file_descriptors(ret):
    
    for fd in ret[0]:
        if fd == p.stdout.fileno():
            read = p.stdout.readline()
            if read:
                sys.stdout.write('stdout: ' + read)
                stdout.append(read)
        if fd == p.stderr.fileno():
            read = p.stderr.readline()
            if read:
                if read.startswith(log_forward_prefix):
                    print "MATCH !!!!!!!"
                    print 'port:', read[len(log_forward_prefix):]
                sys.stderr.write('stderr: ' + read)
                stderr.append(read)


if __name__ == "__main__":




    db = MySQLdb.connect(host="beehive-mysql",    
                         user="waggle",       
                         passwd="waggle",  
                         db="waggle")      

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("SELECT * FROM nodes")


    # get array:
    for row in cur.fetchall():
        print row

    db.close()





    while True:
        p = subprocess.Popen(["/usr/sbin/sshd", "-D", "-e"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout = []
        stderr = []

        while True:
            reads = [p.stdout.fileno(), p.stderr.fileno()]
            ret = select.select(reads, [], [])

            handle_file_descriptors(ret)

            if p.poll() != None:
                time.sleep(3)
                ret = select.select(reads, [], [])
                handle_file_descriptors(ret)
                break

            print 'sshd ended !?'

            print 'stdout:', "".join(stdout)
            print 'stderr:', "".join(stderr)