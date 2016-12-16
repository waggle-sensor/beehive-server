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
    
    nodeId = args.nodeId.lower().rjust(16, '0')   # all nodeId's are in lower case
    nodeId_NoLeadingZeros = re.sub('^0+', '', nodeId)
    print('nodeId_NoLeadingZeros = ', nodeId_NoLeadingZeros)
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
    urlNodePage = 'http://beehive1.mcs.anl.gov/nodes/{node_id}?version=2'.format(node_id = nodeId)
    urlData = CmdString('''/bin/curl -s {url_node} | grep "nodes/" | head -n 1 | grep -Po '"http.*"' '''.format(url_node = urlNodePage))
    print('###################################', urlNodePage)
    lines = CmdList('''curl -s {url_data} | sort | tail -n 100'''.format(url_data = urlData))
    for iLine, line in enumerate(lines):
        print(iLine, line)
    print(CmdString('date -u'))
    
    print('################################### journalctl')
    CmdList('journalctl --since=-2h | grep {} | grep monitor-nodes-logs | tail -n 30'.format(nodeId_NoLeadingZeros))

    print('NUMBER OF journalctl monitor-nodes-logs MESSAGES: ', CmdString('journalctl --since=-3h | grep {} | grep monitor-nodes-logs | wc -l'.format(nodeId_NoLeadingZeros)))

    print('NUMBER OF journalctl monitor-nodes-data MESSAGES: ', CmdString('journalctl --since=-3h | grep {} | grep monitor-nodes-data | wc -l'.format(nodeId_NoLeadingZeros)))

    print('NUMBER OF journalctl       MESSAGES: ', CmdString('journalctl --since=-3h | grep {} | wc -l'.format(nodeId_NoLeadingZeros)))
    print('curl -s {url_data} | sort > {node_id}.txt'.format(url_data = urlData, node_id = nodeId))
    print('###################################')
    print('Node id: {}\n'.format(nodeId))
    print('Cloud Vitals\n')
    print('Reverse Tunnel Port : {}'.format(port))
    print('Node Sensor-data Portal Link : {}'.format(urlNodePage))
    print('Node Log-data Portal Link : {}'.format('COMING SOON'))
    print('Node Liveliness Portal Link : {}'.format('COMING SOON'))

