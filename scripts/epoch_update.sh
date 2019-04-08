#!/bin/bash
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
echo "{" > /mnt/datasets/mcs/epoch/api/1/epoch
echo '  "epoch": '$(date +%s) >> /mnt/datasets/mcs/epoch/api/1/epoch
echo "}" >> /mnt/datasets/mcs/epoch/api/1/epoch

