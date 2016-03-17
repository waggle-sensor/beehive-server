#!/usr/bin/python

import subprocess
import sys
import select
import time
import MySQLdb

log_forward_prefix = 'debug1: Local forwarding listening on 127.0.0.1 port '


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




    # restart loop
    while True:
        p = subprocess.Popen(["/usr/sbin/sshd", "-D", "-e"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout = []
        stderr = []

        # reading loop
        while True:
            reads = [p.stdout.fileno(), p.stderr.fileno()]
            ret = select.select(reads, [], [])

            for fd in ret[0]:
                if fd == p.stdout.fileno():
                    read = p.stdout.readline()
                    if read:
                        sys.stdout.write('stdout: [' + read + ']')
                        stdout.append(read)
                if fd == p.stderr.fileno():
                    read = p.stderr.readline()
                    if read:
                        if read.startswith(log_forward_prefix):
                            print "MATCH !!!!!!!"
                            print 'port:', read[len(log_forward_prefix):]
                        sys.stderr.write('stderr: [' + read+ ']')
                        stderr.append(read)

            if p.poll():
                print '########### sshd ended !?  #############'

                print 'final stdout: [', "".join(stdout) , ']'
                print 'final stderr: [', "".join(stderr) , ']'
                break
                
            time.sleep(1)
            ret = select.select(reads, [], [])
            handle_file_descriptors(ret)
            
            
            
            
            