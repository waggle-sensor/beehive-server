#!/usr/bin/env bash

# create all exchanges
rabbitmqadmin declare exchange type=fanout name=x_data_in
rabbitmqadmin declare exchange type=fanout name=x_data_raw
rabbitmqadmin declare exchange type=fanout name=x_data_decoded

if false
then
    echo 'branch 1'
    python3 queue-print.py   x_data_in   q_data_in  &
else
    echo 'branch 2'
    python3 waggleSend.py -rate 0.1 &
    python3 queue-to-exchange.py    x_data_in       q_data_in   x_data_raw      &
    python3 queue-print.py          x_data_raw      q_db_raw                    &
    python3 queue-to-exchange.py    x_data_raw      q_decode    x_data_decoded  &
    python3 queue-print.py          x_data_decoded  q_plenario                  &
    python3 queue-print.py          x_data_decoded  q_db_decoded                &
    python3 queue-print.py          x_data_raw      q_logfile                   &
    python3 queue-print.py          x_data_raw      q_slack                     &
    python3 queue-print.py          x_data_raw      q_node_status               &
fi
echo 'done'
