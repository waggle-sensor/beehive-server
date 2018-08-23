#!/bin/sh

set -e

url='http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/AoT_Chicago.public.recent.tar'
/home/sean/beehive-server/publishing-tools/bin/build-plenario-json-from-digest-url $url > /tmp/plenario.json
scp /tmp/plenario.json aotpub:/home/waggle/waggle_www/downloads/beehive1/plenario.json
