#!/usr/bin/env python3

import datetime
import json
import os
import re
import subprocess
import sys
import time

#_______________________________________________________________________
# Run a command and capture it's output
def Cmd(command):
    print(' CMD:  ', command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  shell = True,
                                  universal_newlines = True)
    #return iter(p.stdout.readline, b'')
    return p.stdout

#_______________________________________________________________________
if __name__ == '__main__':
    # Read the config file, make sure what we need is there
    with open('/root/git/beehive-server/beehive-config.json', 'r') as f:
        configAll = json.load(f)
    config = configAll['backup']
    del configAll
    print('backup config: ', json.dumps(config, indent = 4))
    pathLocal = config['local directory']
    pathDestination = config['destination']
    sleepSeconds = config['period']
    nFiles = config['number of files']
    
    # Make sure the local backup folder exists, if it doesn't, then create it
    print('local directory :', pathLocal)
    Cmd('mkdir -p ' + pathLocal)
    Cmd('chmod 700 ' + pathLocal)
    print([x for x in Cmd('ls -lr ' + pathLocal + "/..")])
    
    #periodically perform a backup
    while True:
        # create the name of this backup based on date and time
        dtUtcNow = datetime.datetime.utcnow()
        name = dtUtcNow.strftime("%Y-%m-%d_%H-%M-%S")
        pathTemp = '/tmp/' + name
        mysqlFileTemp = pathTemp + '/waggle.sql'
        filenameArchive = pathTemp + '/beehive-backup-' + name + '.tgz'
        # create a temporary directory of the stuff we want to backup, and fill it
        Cmd('mkdir -p ' + pathTemp)
        #    files
        
        #    mysql dump
        Cmd("""docker exec -ti beehive-mysql bash -c 'mysqldump --verbose --user=waggle --password=waggle --add-drop-table --add-locks  --add-drop-database --databases waggle > {}' """.format(mysqlFileTemp))

        # compress the result into a single file
        Cmd("""tar -zcf {} {} /mnt/ssh_keys /mnt/waggle' """.format(filenameArchive, mysqlFileTemp))
        
        # print the contents of the temporary dir
        print([x for x in Cmd('ls ' + pathTemp)])
        
        # copy the result to the destination
        Cmd('scp -v {} {}'.format(filenameArchive, pathDestination))
        
        # delete extra files
        
        # sleep until it is time for another backup
        print('sleeping for {} seconds starting at (roughly) {}...'.format(sleepSeconds, name))
        time.sleep(sleepSeconds)
