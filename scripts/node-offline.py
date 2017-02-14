#!/usr/bin/env python3
""" set or read the OFFLINE status of a node.  The start_time is always the present time.
"""

import argparse
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

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('command', choices = ['set', 'clear', 'list'])
    argParser.add_argument('node_id')    
    argParser.add_argument('--verbose', '-v', action='count')
    args = argParser.parse_args()

    if args.command == 'list':
        result = Cmd('docker exec -ti beehive-mysql mysql  -u waggle --password=waggle -B --disable-column-names -e "SELECT * FROM waggle.node_offline;"')
    else:
        query0 = "DELETE FROM waggle.node_offline WHERE node_id = '{}';".format(args.node_id)
        if args.command == 'set':
            query1 = "INSERT INTO waggle.node_offline (node_id) VALUES ('{}');".format(args.node_id)
        else:
            query1 = ''
        result = Cmd('''docker exec -ti beehive-mysql mysql  -u waggle --password=waggle -e "{}" '''.format(query0 + query1))
        
    for r in result:
        print(r.strip())
    print('')