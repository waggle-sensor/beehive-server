#! /bin/python3
import argparse
import re
import subprocess
import sys
global verbosity
#

#_______________________________________________________________________
# Run a command and capture it's output
def Cmd(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    return iter(p.stdout.readline, b'')

#_______________________________________________________________________
def GetDictNodeToPort():
    global verbosity
    entries = Cmd("get-node-entries")
    #field_names = ("id", "node_id", "project", "description", "reverse_ssh_port", "hostname", "hardware", "name", "location", "last_updated", "opmode")
    dictNodeToPort = {}
    for iEntry, entry in enumerate(entries):
        row = str(entry).split(';')
        dictNodeToPort[row[1].lower()] = int(row[4])
    if verbosity:
        print(dictNodeToPort)
    return dictNodeToPort
  
#_______________________________________________________________________
def GetPortFromNode(nodeId):
    nodeId = nodeId.lower()
    dictNodeToPort = GetDictNodeToPort()
    port = None
    if nodeId in dictNodeToPort:
        port = dictNodeToPort[nodeId]
    return port
  
#_______________________________________________________________________
if __name__ == '__main__':
    global verbosity
    
    # get args
    argParser = argparse.ArgumentParser()
    argParser.add_argument('nodeId')
    argParser.add_argument('--verbose', '-v', action='count')
    args = argParser.parse_args()
    
    nodeId = args.nodeId.lower()   # all nodeId's are in lower case
    verbosity = args.verbose
    
    # make sure the nodeId has the proper structure
    if not re.fullmatch('^[0-9a-zA-Z]{16}$', nodeId):
        message = 'FAIL  - improper structure of nodeId "{}"'.format(args.nodeId)
        sys.exit(message)
    
    port = GetPortFromNode(nodeId)
    if verbosity: print('GetPortFromNode({}) = {}'.format(nodeId, port))
    if port:
        print(port)
    else:
        message = 'FAIL  - no port found for nodeId "{}"'.format(args.nodeId)
        sys.exit(message)

