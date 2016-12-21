#! /bin/python3
import argparse
import datetime
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
# Run a command and capture it's output
def Cmd1(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  shell = True,
                                  universal_newlines = True)
    #return iter(p.stdout.readline, b'')
    return p.stdout

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
    argParser.add_argument('nodeId')
    argParser.add_argument('--verbose', '-v', action='count')
    argParser.add_argument('-gapSeconds', type = int, default = 60, 
                                    help = 'minimum # of seconds between samples to be considered a gap')
    argParser.add_argument('-groupSensors', action = 'store_true', help = 'treats all sensors as one with regard to detecting gaps') 
    argParser.add_argument('-nDays', type = int, default = 1, help = 'number of days back to parse')
    argParser.add_argument('-nLines', type = int, default = 0, help = 'max number of lines to read from data file')
    args = argParser.parse_args()
    
    nodeId = args.nodeId.lower().rjust(16, '0')   # all nodeId's are in lower case
    nodeId_NoLeadingZeros = re.sub('^0+', '', nodeId)
    print('nodeId_NoLeadingZeros = ', nodeId_NoLeadingZeros)
    verbosity = args.verbose
    dtGap = args.gapSeconds
    print('dtGap = ', dtGap)
    
    # make sure the nodeId has the proper structure
    if not re.fullmatch('^[0-9a-zA-Z]{16}$', nodeId):
        message = 'FAIL  - improper structure of nodeId "{}"'.format(args.nodeId)
        sys.exit(message)
    
    # find the reverse ssh port
    port = GetPortFromNode(nodeId)
    if verbosity: print('GetPortFromNode({}) = {}'.format(nodeId, port))
    if port:
        print(' ** Reverse Tunnel Port : {} **'.format(port))
    else:
        message = 'FAIL  - no port found for nodeId "{}"'.format(args.nodeId)
        sys.exit(message)
        
    if True:
        d = {}  # dictionary of gaps
        tNow = datetime.datetime.utcnow()
        tNow.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        dtOneDay = datetime.timedelta(days = 1)
        tStart = tNow - dtOneDay * args.nDays
        
        tCur = tStart
        while tCur <= tNow:
            strDate = DatetimeToDateString(tCur)
            tCur += dtOneDay
            cmd = 'curl -s "http://beehive1.mcs.anl.gov/api/1/nodes/{}/export?date={}&version=2" | sort'.format(args.nodeId, strDate)
            print('cmd = ', cmd)
            for iLine, line in enumerate(Cmd1(cmd)):
                if verbosity: print(iLine, '"' + line.strip() + '"')
                cols = line.split(';')
                try:
                    strTime = cols[0]
                    t = DatetimeFromString(strTime)
                    sensor = cols[2] if not args.groupSensors else 'sensor'
                    if sensor in d:
                        dt = (t - d[sensor]['tLast'])   # timedelta
                        dtSeconds = dt.total_seconds()   # number of seconds since last sample
                        #print('  dtSeconds = ', dtSeconds)
                        if dtSeconds > dtGap:
                            #print('   true assigning...')
                            d[sensor]['gaps'].append((d[sensor]['tLast'], dtSeconds))  # (tStart, duration)
                        else:
                            #print('   false assigning...')
                            d[sensor]['tStepsTotal'] += dt
                            d[sensor]['nSteps'] += 1
                    else:
                        d[sensor] = {}
                        d[sensor]['tFirst'] = t
                        d[sensor]['gaps'] = []
                        d[sensor]['tStepsTotal'] = datetime.timedelta()
                        d[sensor]['nSteps'] = 0
                    d[sensor]['tLast'] = t
                    
                except Exception as e:
                    # ignore bad lines  
                    print('ERROR: line #{} : "{}", "{}"'.format(iLine, line, str(e)))
                    pass    
                if args.nLines != 0 and iLine >= args.nLines:
                    break
        print('FIRST, LAST, LENGTH:----------------------------')
        for sensor in sorted(d.keys()):
            ds = d[sensor]
            print(' {:13s}  {}  {}  {}'.format(sensor,
                        DatetimeToString(ds['tFirst']),               
                        DatetimeToString(ds['tLast']),
                        (ds['tLast'] - ds['tFirst']).total_seconds()))
        print('STEPS:  AVG, GAPS ----------------------------------------')
        for sensor in sorted(d.keys()):
            ds = d[sensor]
            gaps = ds['gaps']
            avgGap = 0
            if ds['nSteps']:
                avgGap = float(ds['tStepsTotal'].total_seconds()) / float(ds['nSteps'])
            #print(sensor, 'avg gap = {:f}s, gaps = '.format(avgGap), ds['gaps'])
            print('{:13s}  {:>10.3f}s, '.format(sensor, avgGap), sorted([x[1] for x in ds['gaps']], reverse = True))
            #[sensor, ':', 'firstd[sensor]) #sorted([x[1] for x in d[sensor]['gaps']))
        print('GAPS: DURATION, START, END----------------------------------------')
        for sensor in sorted(d.keys()):
            ds = d[sensor]
            gaps = ds['gaps']
            if len(gaps):
                sensorName = sensor
                for gap in gaps:
                    print('{:13s} {:>10.2f}    {}   {}'.format(sensorName, gap[1], gap[0], gap[0] + datetime.timedelta(seconds = gap[1])))
                    sensorName = ' '
        print('----------------------------------------')
            
    if True:
        # get the last sensor-data samples from the node.
        # 'head' gets the 1st appearing url, which should correspond to the latest date
        # 'tail' limits the output to the last lines, the last set of sensor readings
        urlNodePage = 'http://beehive1.mcs.anl.gov/nodes/{node_id}?version=2'.format(node_id = nodeId)
        urlData = CmdString('''/bin/curl -s {url_node} | grep "nodes/" | head -n 1 | grep -Po '"http.*"' '''.format(url_node = urlNodePage))
        print('###################################')
        lines = CmdList('''curl -s {url_data} | sort | tail -n 10'''.format(url_data = urlData))
        for iLine, line in enumerate(lines):
            print(iLine, line)
        print(CmdString('date -u'))
        
    if True:
        print('################################### journalctl')
        CmdList('journalctl --utc --since=-2h | grep {} | grep monitor-nodes-logs | tail -n 30'.format(nodeId_NoLeadingZeros))

        print('NUMBER OF journalctl monitor-nodes-logs MESSAGES: ', CmdString('journalctl --utc --since=-3h | grep {} | grep monitor-nodes-logs | wc -l'.format(nodeId_NoLeadingZeros)))

        print('NUMBER OF journalctl monitor-nodes-data MESSAGES: ', CmdString('journalctl --utc --since=-3h | grep {} | grep monitor-nodes-data | wc -l'.format(nodeId_NoLeadingZeros)))

        print('NUMBER OF journalctl       MESSAGES: ', CmdString('journalctl --utc --since=-3h | grep {} | wc -l'.format(nodeId_NoLeadingZeros)))
        print('curl -s {url_data} | sort > {node_id}.txt'.format(url_data = urlData, node_id = nodeId))
        print('###################################')
        print('Node id: {}\n'.format(nodeId))
        print('Cloud Vitals\n')
        print('Reverse Tunnel Port : {}'.format(port))
        print('Node Sensor-data Portal Link : {}'.format(urlNodePage))
        print('Node Log-data Portal Link : {}'.format('COMING SOON'))
        print('Node Liveliness Portal Link : {}'.format('COMING SOON'))

