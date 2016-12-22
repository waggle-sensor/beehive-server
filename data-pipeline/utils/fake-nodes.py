#! /bin/python3
import argparse
import datetime
import re
import subprocess
import sys

global verbosity

""" Generates text to stdout that can be executed at the shell on a beehive server to
    generate fake nodes and data for testing.
    Specify the number of nodes, number of days and number of samples per day.
"""
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
# Run a command and capture it's output - return iterable like result of open()
def Cmd1(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  shell = True,
                                  universal_newlines = True)
    #return iter(p.stdout.readline, b'')
    return p.stdout
 
#_______________________________________________________________________
def GetPortFromNode(nodeId):
    nodeId = nodeId.lower()
    dictNodeToPort = GetDictNodeToPort()
    port = None
    if nodeId in dictNodeToPort:
        port = dictNodeToPort[nodeId]
    return port

    
#_______________________________________________________________________
def DatetimeFromString(strTime):
    if len(strTime) == 19:
        result = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")
    else:
        result = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S.%f")
    return result
#_______________________________________________________________________
def DatetimeToString(t):
    return t.strftime("%Y-%m-%d %H:%M:%S.%f")
#_______________________________________________________________________
def DatetimeToDateString(t):
    return t.strftime("%Y-%m-%d")

#_______________________________________________________________________
#_______________________________________________________________________
if __name__ == '__main__':
    global verbosity
    
    print('###################################\n' * 3)

    # get args
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--nNodes', type = int, default = 1)
    argParser.add_argument('--nDays', type = int, default = 1)
    argParser.add_argument('--nSamplesPerDay', type = int, default = 1)
    argParser.add_argument('--nSecondsBetweenSamples', type = int, default = 1)
    argParser.add_argument('--verbose', '-v', action='count')
    args = argParser.parse_args()

    dtDay = datetime.timedelta(days = 1)
    dtSample = datetime.timedelta(seconds = args.nSecondsBetweenSamples)

    for iNode in range(1, args.nNodes + 1):
        nodeId = '{}'.format(iNode).rjust(4, '0').rjust(16, 'f')
        print('### node #{}: {}'.format(iNode, nodeId))

        # create node
        cmd = '''docker exec -ti beehive-mysql mysql  -u waggle --password=waggle -e "use waggle; INSERT INTO nodes (node_id, hostname, project, description, reverse_ssh_port, hardware, name, location) VALUES ('{node_id}', '{hostname}', {iNode}, '{description}', {reverse_ssh_port}, '{hardware}', '{name}', '{location}');"'''.format(
            iNode = iNode,
            node_id = nodeId,
            hostname = 'hostname{}'.format(iNode),
            project = 'project{}'.format(iNode),
            description = 'description{}'.format(iNode),
            reverse_ssh_port = '{}'.format(iNode),
            hardware = '{{ \\"hw\\" : \\"hw{}\\" }}'.format(iNode),
            name = 'name{}'.format(iNode),
            location = 'location{}'.format(iNode))
        print(cmd)
        
        #create data for node
        t0 = DatetimeFromString('2016-01-01 01:00:00')
        for iDay in range(args.nDays):
            t = t0 + iDay * dtDay
            for iSample in range(args.nSamplesPerDay):
                print('###     day {:02d},  sample {:02d}'.format(iDay, iSample))
                
                # raw data
                cmd =  '''docker exec -it beehive-cassandra cqlsh -e "USE waggle; INSERT INTO sensor_data_raw (node_id, date, ingest_id, plugin_name, plugin_version, plugin_instance, timestamp, parameter, data) VALUES ('{nodeName}', '{date}', 0, 'pluginName', 'pluginVersion',  'pluginInstance', '{timestamp}', 'param', 'data');"'''.format(
                    nodeName = nodeId,
                    date = DatetimeToDateString(t),
                    timestamp = DatetimeToString(t),
                )
                print(cmd)

                #decoded data
                cmd =  '''docker exec -it beehive-cassandra cqlsh -e "USE waggle; INSERT INTO sensor_data_decoded (node_id, date, ingest_id, meta_id, timestamp, data_set, sensor, parameter, data, unit) VALUES ('{nodeName}', '{date}', 0, 0, '{timestamp}', 'data_set', 'sensor', 'param', 'data', 'unit0');"'''.format(
                    nodeName = nodeId,
                    date = DatetimeToDateString(t),
                    timestamp = DatetimeToString(t),
                )
                print(cmd)
                
                t += dtSample
