#!/usr/bin/env python3
""" set or read the OFFLINE status of a node.  The start_time is always the present time.
"""

import argparse
import datetime
import subprocess

#_______________________________________________________________________
# Run a command and capture it's output
def Cmd(command, bPrint = False):
    if bPrint:
        print(' CMD:  ', command)
        
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  shell = True,
                                  universal_newlines = True)
    if bPrint: print("Cmd: ", command)
    #return iter(p.stdout.readline, b'')
    return p.stdout

def Query(query, bPrint = True):
    result = Cmd('''docker exec -ti beehive-mysql mysql  -u waggle --password=waggle -e "{}" '''.format(query))
    if bPrint:
        for x in result:
            print(x.strip())
    
if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-off', action = 'append', help = 'sets a node to "offline" state')
    argParser.add_argument('-on',  action = 'append', help = 'sets a node to "online" state')
    argParser.add_argument('-l', '--list', action = 'store_true', help = 'lists the offline nodes')    
    argParser.add_argument('--verbose', '-v', action='count')
    args = argParser.parse_args()
    if args.verbose: print('args = ', args)
    if args.verbose: print(datetime.datetime.utcnow())

    nodesOnAndOff = []
    if args.on: nodesOnAndOff.extend(args.on)
    if args.off: nodesOnAndOff.extend(args.off)
    for node in nodesOnAndOff:
        Query("DELETE FROM waggle.node_offline WHERE LOWER(node_id) = '{}';".format(node.lower()))

    if args.off:        # add the offline nodes to the table
        for node in args.off:
            Query("INSERT INTO waggle.node_offline (node_id) VALUES ('{}');".format(node.lower()))
        
    if args.list:
        Query("SELECT * FROM waggle.node_offline;")
    print('')
