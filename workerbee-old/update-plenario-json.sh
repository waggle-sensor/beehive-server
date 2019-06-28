#!/bin/sh
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

set -e

url='http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/AoT_Chicago.public.recent.tar'
/home/sean/beehive-server/publishing-tools/bin/build-plenario-json-from-digest-url $url > /tmp/plenario.json
scp /tmp/plenario.json aotpub:/home/waggle/waggle_www/downloads/beehive1/plenario.json
