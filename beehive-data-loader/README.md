# Beehive Data Loader

This is service moves raw message data from RabbitMQ to Cassandra in our v2 data pipeline.


Prometheus Metrics Endpoint

∙ Job Name: data_loader
∙ Target: 127.0.0.1:9101
∙ Data: By visiting 127.0.0.1:9101, you can access to metrics like these:
    # HELP dataloader_message_counter_0000000000000001_total This metric counts the number of the messages for each node.
    # TYPE dataloader_message_counter_0000000000000001_total counter
    dataloader_message_counter_0000000000000001_total{counter_type="message"} 144.0
    ....
    # HELP dataloader_message_counter_0000000000000002_total This metric counts the number of the messages for each node.
    # TYPE dataloader_message_counter_0000000000000002_total counter
    dataloader_message_counter_0000000000000002_total{counter_type="message"} 145.0

Each counter and error metric name contains a node ID.

