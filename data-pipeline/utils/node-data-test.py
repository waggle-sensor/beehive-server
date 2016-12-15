#! /bin/python3
import argparse
import re
import subprocess
import sys

global verbosity

#_______________________________________________________________________
# Run a command, return its output as a single string
def CmdString(command):
    return subprocess.getoutput(command)

#_______________________________________________________________________
# Run a command, return the output as a list of strings
def CmdList(command, bDebug = True):
    strResult = subprocess.getoutput(command)
    if bDebug:
        print('CmdList:   command = ', command,'\n   strResult = ', strResult)
    if len(strResult):
        result = strResult.split('\n')
    else:
        result = []
    return result

#_______________________________________________________________________
# Run a command and capture it's output
def Cmd0(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    return iter(p.stdout.readline, b'')

#_______________________________________________________________________
# Run a command and capture it's output.
# command is a string, which can include pipes.
# the return value is a single string - where lines are delimited with '\n'
def RRun(command):
    lines = Cmd2(command)
    #print(lines)
    return lines
    '''
    for iLine, line in enumerate(lines):
        if nLines > 0 and iLine >= nLines:
            break
        print(iLine, line)
    '''
#_______________________________________________________________________
def GetDictNodeToPort():
    global verbosity
    entries = CmdList("get-node-entries", bDebug = False)
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
        print(' ** Reverse Tunnel Port : {} **'.format(port))
    else:
        message = 'FAIL  - no port found for nodeId "{}"'.format(args.nodeId)
        sys.exit(message)

    # get the last sensor-data samples from the node.
    # 'head' gets the 1st appearing url, which should correspond to the latest date
    # 'tail' limits the output to the last lines, the last set of sensor readings
    urlData = 'http://beehive1.mcs.anl.gov/nodes/{node_id}?version=2'.format(node_id = nodeId)
    print('###################################', urlData)
    lines = CmdList('''/bin/curl -s {url_data} | grep "nodes/" | head -n 1 | grep -Po '"http.*"' | xargs curl -s | sort | tail -n 100'''.format(url_data = urlData))
    for iLine, line in enumerate(lines):
        print(iLine, line)
    print(CmdString('date -u'))
    
    print('################################### journalctl')
    print(CmdString('journalctl --since=-2h -u beehive-nginx | grep {} | tail -n 30'.format(nodeId)))
    print('NUMBER OF journalctl MESSAGES: ', CmdString('journalctl --since=-3h -u beehive-nginx | grep {} | wc -l'.format(nodeId)))
    print('###################################'.format(port))
    print('Node id: {}\n'.format(nodeId))
    print('Reverse Tunnel Port : {}'.format(port))
    print('Node Sensor-data Portal Link : {}'.format(urlData))
    print('Node Log-data Portal Link : {}'.format('COMING SOON'))
    print('Node Liveliness Portal Link : {}'.format('COMING SOON'))

