#!/bin/bash
echo "{" > /mnt/datasets/mcs/epoch/api/1/epoch
echo '  "epoch": '$(date +%s) >> /mnt/datasets/mcs/epoch/api/1/epoch
echo "}" >> /mnt/datasets/mcs/epoch/api/1/epoch

