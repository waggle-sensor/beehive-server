#!/usr/bin/env python3
""" gather data for troubleshooting the 9 CDOT nodes.
"""

import argparse
import datetime
import subprocess

# select node_id from nodes where description like "AoT Chicago%" and location not like "TCS%" and location not like "Lost%";
nodes = '''0000001e061089fa
             0000001e0610893c
             0000001e06107e5d
             0000001e0610bbe9
             0000001e0610b9fd
             0000001e0610b9e1
             0000001e0610ba60
             0000001e0610b9e7
             0000001e0610b9f8'''.lower().split()

heartbeatModes = {
    "0000001e0610893c" : "N/A (Ubuntu 14)",
    "0000001e0610ba93" : "always         ",
    "0000001e0610ba89" : "wellness       ",
    "0000001e0610b9fd" : "wellness       ",
    "0000001e0610bbff" : "wellness       ",
    "0000001e0610bbf9" : "wellness       ",
    "0000001e0610ba3f" : "always         ",
    "0000001e0610ba37" : "wellness       ",
    "0000001e0610ba8b" : "wellness       ",
    "0000001e0610bbe9" : "wellness       ",
    "0000001e0610ba3b" : "wellness       ",
    "0000001e0610ba8f" : "wellness       ",
    "0000001e06108905" : "always         ",
    "0000001e0610ba67" : "always         ",
    "0000001e0610ba13" : "wellness       ",
    "0000001e0610bc10" : "wellness       ",
    "0000001e0610ba46" : "always         ",
    "0000001e061089e5" : "always         ",
    "0000001e0610bbf5" : "always         ",
    "0000001e0610ba18" : "wellness       ",
    "0000001e06107e5d" : "N/A (Ubuntu 14)",
    "0000001e06107d97" : "always         ",
}             

attStatuses = {
    "0000001e0610893c" : {"sim_iccid" : "89011702272021567182", "inSession" : True , "usageMB" : 160.141 , 'testsPassed' : 4},
    "0000001e06107e5d" : {"sim_iccid" : "89011702272021567588", "inSession" : False, "usageMB" : 0       , 'testsPassed' : 3},
    "0000001e0610bbe9" : {"sim_iccid" : "89011702272021567562", "inSession" : False, "usageMB" : 0       , 'testsPassed' : 2},
    "0000001e0610b9fd" : {"sim_iccid" : "89011702272021567232", "inSession" : False, "usageMB" : 0       , 'testsPassed' : 3},
    "0000001e0610b9e1" : {"sim_iccid" : "89011702272021567570", "inSession" : False, "usageMB" : 0       , 'testsPassed' : 2},
    "0000001e0610ba60" : {"sim_iccid" : ""                    , "inSession" : False, "usageMB" : 0       , 'testsPassed' : 0},
    "0000001e0610b9e7" : {"sim_iccid" : "89011702272021567216", "inSession" : False, "usageMB" : 0       , 'testsPassed' : 2},
    "0000001e0610b9f8" : {"sim_iccid" : "89011702272021567547", "inSession" : False, "usageMB" : 0       , 'testsPassed' : 3},
}             
             
#_______________________________________________________________________
# Run a command, return its output as a single string
def CmdString(command, bPrint = True):
    if bPrint:
        print("\n CMD :\n{}\n".format(command))

    result = subprocess.getoutput(command)
    #result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, universal_newlines = True);

    #result = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, universal_newlines = True);
    if bPrint:
        print("\n RESULT :\n{}\n".format(result))
    return result

#_______________________________________________________________________
# Run a command, return the output as a list of strings
def CmdList(command, bPrint = True):
    strResult = CmdString(command, bPrint = bPrint)
    if len(strResult):
        result = strResult.split('\n')
    else:
        result = []
    return result

    #_______________________________________________________________________
def Query(query, bPrint = True):
    theCommand = '''docker exec -t beehive-mysql mysql -sN -u waggle --password=waggle waggle -e "{}"  '''.format(query)
    result0 = CmdString(theCommand, bPrint = bPrint)
    result = ''.join([x for x in result0.split('\n') if not x.startswith("mysql: [Warning] ")])
    return result

#_______________________________________________________________________
if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--verbose', '-v', action='count', default=0, help='need at least 1 to generate all output')
    args = argParser.parse_args()
    if args.verbose: print('args = ', args)
    if args.verbose: print('utcnow = ', datetime.datetime.utcnow())
    
    nMonths = 3
    
    print(""" testsPassed:
            0 = none
            1 = provisionin
            2 = SIM / Device
            3 = Network Connection
            4 = IP / Internet""")
    for iNode, node in enumerate(nodes):
        attStatus = ("", "", "")
        if node in attStatuses:
            a = attStatuses[node]
            attStatus = ('yes' if a['inSession'] else 'no', a['usageMB'], a['testsPassed'])
        print ('{}\n{}. node = {},   heartbeat = {},  inSession={},   Cycle-to-Date-Usage(MB)={}, testsPassed = {}'.format(
            '-'*70, iNode, node, 
            heartbeatModes.get(node, 'UNKNOWN').strip(),
            attStatus[0], 
            attStatus[1], 
            attStatus[2]))
        
        # get the sim_iccid
        sim_iccid = Query('''SELECT sim_iccid FROM node_management WHERE node_id = '{}' '''.format(node), bPrint=False)
        print('#### sim_iccid = "{}"'.format(sim_iccid))
        
        # get journalctl beehive-nginx
        if args.verbose > 0:
            CmdString("""journalctl --since="{} months ago" -u beehive-nginx | grep "{}" """.format(nMonths, node))
    
    if args.verbose > 0:
        # get sshd log
        CmdString("""journalctl -u beehive-sshd """)

        # get rabbitmq log
        CmdString("""journalctl -u beehive-rabbitmq  """)

        