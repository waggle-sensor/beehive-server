#!/usr/bin/env bash

# delete all exchanges
rabbitmqadmin delete exchange name=x_data_in
rabbitmqadmin delete exchange name=x_data_raw
rabbitmqadmin delete exchange name=x_data_decoded

rabbitmqadmin delete queue name=q_data_in
rabbitmqadmin delete queue name=q_db_raw
rabbitmqadmin delete queue name=q_decode
rabbitmqadmin delete queue name=q_logfile
rabbitmqadmin delete queue name=q_slack
rabbitmqadmin delete queue name=q_node_status
rabbitmqadmin delete queue name=q_plenario
rabbitmqadmin delete queue name=q_db_decoded

# temporary hack to kill WaggleSend.py
pkill python3