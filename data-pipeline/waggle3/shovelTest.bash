#!/usr/bin/env bash

# This test illustrates the implementation and behavior of the rabbitmq plugin, shovel.
# It uses a dynamic shovel, which is created, allowed to run for a time, then deleted.
# All rabbitmq structures are declared in the beginning, and deleted at the end.
# NOTE: Must be run by root (or possibly with modified permissions).

#delete test structures
function delete_all() {
    rabbitmqadmin delete exchange name="x-src"
    rabbitmqadmin delete queue    name="q-src"
    rabbitmqadmin delete queue    name="q-src2"
    rabbitmqadmin delete exchange name="x-dest"
    rabbitmqadmin delete queue    name="q-dest"
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

set -v -x

delete_all
list_all

#create test src queue
rabbitmqadmin declare exchange  name="x-src" type=fanout durable=true
rabbitmqadmin declare queue     name="q-src" durable=true
rabbitmqadmin declare queue     name="q-src2" durable=true
rabbitmqadmin declare binding   source="x-src" destination_type="queue" destination="q-src"  routing_key="q-src"
rabbitmqadmin declare binding   source="x-src" destination_type="queue" destination="q-src2" routing_key="q-src"

#create test dest queue
rabbitmqadmin declare exchange  name="x-dest" type=fanout durable=true
rabbitmqadmin declare queue     name="q-dest" durable=true

list_all

#create a bunch of messages on src
for i in {1..3}; do
    echo "msg_${i}"
    rabbitmqadmin publish exchange=x-src routing_key=q-src payload="msg_${i}"
done

sleep 3
echo "BEFORE SHOVEL CREATED"    
print_all_messages

rabbitmqctl set_parameter shovel my-shovel \
    '{"src-uri": "amqp://", \
    "src-queue": "q-src", \
    "dest-uri": "amqp://", \
    "dest-queue": "q-dest"}'

rabbitmqctl list_parameters
    
sleep 2
echo "AFTER SHOVEL CREATED"    
print_all_messages

# clean up shovel    
echo "DELETE SHOVEL"
rabbitmqctl clear_parameter shovel my-shovel
rabbitmqctl list_parameters
rabbitmqadmin publish exchange=x-src routing_key=q-src payload="should NOT be shoveled"
sleep 3
echo "AFTER SHOVEL DELETED"    
print_all_messages
delete_all
list_all