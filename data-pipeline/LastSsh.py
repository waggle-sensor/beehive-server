#!/usr/bin/env python3

# LastUpdate.py
import argparse
import datetime
import logging 
import subprocess 
import time
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)

logger = logging.getLogger('beehive-last-ssh')
logger.setLevel(logging.DEBUG)

""" get list of nodes and their ports
    try to ssh into that node
    if it succeeds, store the time to the database
"""
#_______________________________________________________________________
# Run a command and capture it's output
def Cmd(command, bPrint = False):
    if bPrint:
        print(' CMD:  ', command)
        
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  shell = True,
                                  universal_newlines = True)
    #return iter(p.stdout.readline, b'')
    return p.stdout
#_______________________________________________________________________
if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--verbose', '-v', action='count')
    args = argParser.parse_args()
    verbosity = 0 if not args.verbose else args.verbose

    sleepSeconds = 300
    while True:
        tStart = datetime.datetime.utcnow()
        if verbosity: print('starting ssh test of nodes at UTC', tStart)
        nSuccess = 0
        nNodes = 0
        nodeInfos = Cmd('/usr/bin/docker exec -t beehive-mysql mysql  -u waggle --password=waggle -B --disable-column-names -e "SELECT node_id, reverse_ssh_port FROM waggle.nodes;"')
        for nodeInfo in nodeInfos:
            #print('nodeInfo = ', nodeInfo)
            values = nodeInfo.split()
            if len(values) == 2: # and values[1] == '50027':
                node_id, port = values
                try:
                    nNodes += 1
                    # sshpass is used to pass a bogus password of "" in case the node is improperly configured to require the password to be entered
                    cmd = """/bin/sshpass -p "" /bin/ssh -o StrictHostKeyChecking=no -o ProxyCommand='/usr/bin/docker exec -i beehive-sshd nc -q0 localhost {}' -i /mnt/ssh_keys/id_rsa_waggle_aot_ping waggle@ -- date 2> /dev/null""".format(port)
                    if verbosity > 1: print('   try {}  {}...'.format(node_id, port))
                    #print('    ', cmd)
                    output = subprocess.check_output(cmd, shell = True, universal_newlines = True, timeout = 20)
                    if verbosity > 0: print('{:>3d}. {}   {}'.format(nSuccess, node_id, output.strip()))
                    nSuccess += 1
                    
                    # if the command succeeds (no exception) write the value to the database
                    if False:
                        # for some reason, this generates times that are UTC+6 (our timezone is UTC-6, so maybe the offset is added twice???)
                        timestamp = int(datetime.datetime.utcnow().timestamp() * 1000)
                        cmd = '''/bin/docker exec -t beehive-cassandra cqlsh -e "INSERT INTO waggle.nodes_last_ssh (node_id, last_update) VALUES ('{}', {})" '''.format(node_id, timestamp)
                    else:
                        cmd = '''/bin/docker exec -t beehive-cassandra cqlsh -e "INSERT INTO waggle.nodes_last_ssh (node_id, last_update) VALUES ('{}', toUnixTimestamp(now()))" '''.format(node_id)

                    Cmd(cmd)
                except:
                    pass
        if verbosity > 1:    
            results = Cmd('''/bin/docker exec -it beehive-cassandra cqlsh -e "SELECT * FROM waggle.nodes_last_ssh" ''')
            for x in results:
                print(x)
        tEnd = datetime.datetime.utcnow()
        dtProcess = tEnd - tStart
        if verbosity: print('finished ssh test of nodes at UTC', tEnd)
        print('################## all nodes ssh-tested in ', dtProcess, '. {} / {} successes.  sleeping {}s ...'.format(nSuccess, nNodes, sleepSeconds))
        
        time.sleep(sleepSeconds)
        
