#!/usr/bin/env bash

# delete all exchanges
rabbitmqadmin delete exchange name=data-pipeline-in
rabbitmqadmin delete exchange name=decoded

rabbitmqadmin delete queue name=db-raw
if false; then
  rabbitmqadmin delete queue name=q_db_raw
  rabbitmqadmin delete queue name=q_decode
  rabbitmqadmin delete queue name=q_logfile
  rabbitmqadmin delete queue name=q_slack
  rabbitmqadmin delete queue name=q_node_status
  rabbitmqadmin delete queue name=q_plenario
  rabbitmqadmin delete queue name=q_db_decoded
fi

# temporary hack to kill WaggleSend.py
pkill python3

echo 'done'
