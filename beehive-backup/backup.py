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
# bPrintAll should be True only if the caller is not interested in the output, and wants to print the output
def Cmd(command, bPrintAll=True):
    #print(' CMD:  ', command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  shell = True,
                                  universal_newlines = True)
    #return iter(p.stdout.readline, b'')
    
    if bPrintAll:
        # We may need to print all the output to ensure proper blocking until the operation is finished
        for line in p.stdout:
            print(line)
    return p.stdout
#_______________________________________________________________________
def DatetimeToNameAndFilename(t):
    name = t.strftime("%Y-%m-%d_%H-%M-%S")
    filename = 'beehive-backup-{}\.tgz'.format(name)
    return name, filename
#_______________________________________________________________________
def FilenameToDatetime(s):
    t = None
    match = re.search('beehive-backup-([0-9]{4})-([0-9]{2})-([0-9]{2})_([0-9]{2})-([0-9]{2})-([0-9]{2})\.tgz', f)
    groups = match.groups()
    if len(groups) == 6:
        (myYear, myMonth, myDay, myHour, myMinute, mySecond) = (int(x) for x in groups)
        t = datetime.datetime(year = myYear, month = myMonth, day = myDay, 
            hour = myHour, minute = myMinute, second = mySecond)
    return t

#_______________________________________________________________________
if __name__ == '__main__':
    # Read the config file, make sure what we need is there
    with open('/mnt/beehive/beehive-config.json', 'r') as f:
        configAll = json.load(f)
    config = configAll['backup']
    del configAll
    print('backup config: \n' + json.dumps(config, indent = 4))
    pathLocal = config['local directory']
    destUsername = config['dest username']
    destUrl = config['dest url']
    destDir = config['dest dir']
    destCompletePath = destUsername + '@' + destUrl + ':' + destDir
    sleepSeconds = int(config['period'])
    dtBetweenBackups = datetime.timedelta(seconds = sleepSeconds)
    nFiles = config['number of files']
    
    # Make sure the local backup folder exists, if it doesn't, then create it
    print('local directory :', pathLocal)
    Cmd('mkdir -p ' + pathLocal)
    Cmd('chmod 700 ' + pathLocal)
    print([x for x in Cmd('ls -lr ' + pathLocal + "/..", bPrintAll=False)])
    
    # Make sure the remote backup folder exists, if it doesn't, then create it
    print('remote directory :', destCompletePath)
    Cmd("ssh {}@{} 'mkdir -p {dir}; chmod 700 {dir}'".format(destUsername, destUrl, dir = destDir))

    #periodically perform a backup
    while True:
        print('###########################\n-------- ', datetime.datetime.utcnow())
        # get the list of existing backups
        filesExisting = Cmd('ssh {}@{} ls {}/*.tgz'.format(destUsername, destUrl, destDir), bPrintAll=False)
        existingBackups = []
        for f in filesExisting:
            t = FilenameToDatetime(f)
            if t:
                existingBackups.append(t)
        nExisting = len(existingBackups)
        print('\nBEFORE:\nExisting backups:\n\t' + '\n\t'.join([DatetimeToNameAndFilename(x)[0] for x in existingBackups]))

        if nExisting > 0:
            existingBackups.sort(reverse = True)  # 0th item is latest
            nToDelete = nExisting - nFiles + 1
            print('   nExisting = {}, nToDelete = {}'.format(nExisting, nToDelete))
            
            # delete extra files
            while nToDelete > 0:
                nToDelete -= 1
                t = existingBackups.pop()
                Cmd("ssh {user}@{url} rm {dir}/{fn}".format(user = destUsername, url = destUrl, dir = destDir, fn = DatetimeToNameAndFilename(t)[1]))

        # see if enough time passed since the most recent backup to store a new one
        if len(existingBackups) > 0:
            tUtcNow = datetime.datetime.utcnow()
            tNextBackup = existingBackups[0] + dtBetweenBackups
            if tUtcNow < tNextBackup:
                sleepRemainderSeconds = min((tNextBackup - tUtcNow).total_seconds(), 3600)
                time.sleep(sleepRemainderSeconds)
                continue

        # Do a backup now!
        # create the name of this backup based on date and time
        tUtcNow = datetime.datetime.utcnow()
        name, filename = DatetimeToNameAndFilename(tUtcNow)
        pathTemp = '/mnt/beehive-backup-tmp/'
        mysqlFileTemp = pathTemp + 'waggle.sql'
        filenameArchive = pathTemp + filename
        
        # create a temporary directory of the stuff we want to backup, 
        # delete its contents if it is full from last iteration
        Cmd('mkdir -p {0}; rm {0}/*'.format(pathTemp))
        
        #    mysql dump
        Cmd("""docker exec -ti beehive-mysql bash -c 'mysqldump --verbose --user=waggle --password=waggle --add-drop-table --add-locks  --add-drop-database --databases waggle' > {} """.format(mysqlFileTemp))

        # compress the result into a single file
        Cmd("""tar -zcf {} {} /mnt/ssh_keys /mnt/waggle""".format(filenameArchive, mysqlFileTemp))
        
        # print the contents of the temporary dir
        print('TEMP dir:  ', [x for x in Cmd('ls ' + pathTemp)])
        
        # copy the result to the destination
        cmd0 = 'scp -v {} {}'.format(filenameArchive, destCompletePath)
        cmd1 = 'ssh {}@{} ls -ahl {}'.format(destUsername, destUrl, destDir)
        cmd = cmd0 + ';' + cmd1
        #print('\nAFTER creating new backup:\n' + '\n\t'.join([DatetimeToNameAndFilename(FilenameToDatetime(x))[0] for x in Cmd(cmd)]))
        print('\nAFTER creating new backup:\n\t' + '\t'.join([x for x in Cmd(cmd, bPrintAll=False)]))
        
        # sleep until it is time for another backup
        print('sleeping for {} seconds starting at (roughly) {}...'.format(sleepSeconds, name))
        time.sleep(sleepSeconds)
