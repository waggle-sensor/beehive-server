#!/usr/bin/env bash

# TODO: delivery mode=2

#delete test structures
function delete_all() {
    rabbitmqadmin delete exchange name="x-src"
    rabbitmqadmin delete queue    name="q-src"
    rabbitmqadmin delete queue    name="q-src2"
    rabbitmqadmin delete exchange name="x-backup"
    rabbitmqadmin delete queue    name="q-backup"
    rabbitmqctl clear_parameter shovel my-shovel
}

function list_all() {
    rabbitmqadmin list queues
    rabbitmqadmin list exchanges
    rabbitmqadmin list bindings
}

function print_all_messages() {
    rabbitmqadmin list queues vhost name node messages message_stats.publish_details.rate
    for i in {1..4}; do
        rabbitmqadmin get queue="q-src2" requeue=true
    done
}

trace on

delete_all
list_all

#create test src queue
rabbitmqadmin declare exchange  name="x-src" type=fanout durable=true
rabbitmqadmin declare queue     name="q-src" durable=true
rabbitmqadmin declare queue     name="q-src2" durable=true
rabbitmqadmin declare binding   source="x-src" destination_type="queue" destination="q-src"  routing_key="q-src"
rabbitmqadmin declare binding   source="x-src" destination_type="queue" destination="q-src2" routing_key="q-src"

#create test dest queue
rabbitmqadmin declare exchange  name="x-backup" type=fanout durable=true
rabbitmqadmin declare queue     name="q-backup" durable=true

list_all

#create a bunch of messages on src
for i in {1..3}; do
    echo "msg_${i}"
    rabbitmqadmin publish exchange=x-src routing_key=q-src payload="msg_${i}"
done

sleep 3
echo "BEFORE SHOVEL"    
print_all_messages

rabbitmqctl set_parameter shovel my-shovel \
    '{"src-uri": "amqp://", \
    "src-queue": "q-src", \
    "dest-uri": "amqp://", \
    "dest-queue": "q-backup"}'

rabbitmqctl list_parameters
    
sleep 2
echo "AFTER SHOVEL"    
print_all_messages

# clean up shovel    
echo "DELETE SHOVEL"
rabbitmqctl clear_parameter shovel my-shovel
rabbitmqctl list_parameters
rabbitmqadmin publish exchange=x-src routing_key=q-src payload="should NOT be shoveled"
sleep 3
rabbitmqadmin list queues vhost name node messages
print_all_messages
delete_all
