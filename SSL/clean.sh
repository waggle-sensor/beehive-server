#!/bin/bash

cd /usr/lib/waggle/SSL
rm -rf server
cd waggleca
rm -rf certs private
rm serial* index.* cacert*
