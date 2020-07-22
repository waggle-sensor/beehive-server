# Beehive Data Loader

This is service moves raw message data from RabbitMQ to Cassandra in our v2 data pipeline.



## Prometheus Metrics Endpoint


- Job Name: data_loader
- Target: 127.0.0.1:9101
- Data: By visiting 127.0.0.1:9101, you can access metrics like these:
    ```
    # HELP dataloader_message_counter_total This metric counts the number of messages for each node.
    # TYPE dataloader_message_counter_total counter
    dataloader_message_counter_total{node_id="00000000000000015"} 340.0
    dataloader_message_counter_total{node_id="00000000000000016"} 330.0
    dataloader_message_counter_total{node_id="00000000000000013"} 372.0
    
    ...

    # HELP dataloader_error_counter_total This metric counts the number of errors for each node.
    # TYPE dataloader_error_counter_total counter
    dataloader_error_counter_total{node_id="0000000000000005"} 4.0
    dataloader_error_counter_total{node_id="00000000000000014"} 2.0
    dataloader_error_counter_total{node_id="00000000000000010"} 1.0
    dataloader_error_counter_total{node_id="0000000000000006"} 2.0

    ...

    ```


