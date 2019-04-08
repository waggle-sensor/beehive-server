#!/usr/bin/env python
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
import fileinput
from systemd import journal
import re
import sys
import os


identifier = os.environ.get('CONTAINER')
pattern = re.compile('^<([0-9])>(.*)$')

for line in fileinput.input():
    line = line.strip()

    match = pattern.search(line)

    if match is not None:
        priority = int(match.group(1))
        message = match.group(2)
    else:
        priority = 6
        message = line

    journal.send(message, PRIORITY=priority, CONTAINER=identifier, SYSLOG_IDENTIFIER=identifier)
