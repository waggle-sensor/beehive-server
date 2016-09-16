The files in this directory contain the modifications to the beehive server that
implement the 2nd pipeline, which is based on rabbitmq.
Some of these changes were made manually, and need to be integrated into the 
canonical beehive-server code and documentation. 

Databases
Run createTables[ Mysql | Cassandra ].sql


Rabbitmq stuff
    Running and Terminating
        start.bash - to start the pipeline
        stop.bash - to stop the pipeline and delete all rabbitmq structures (queues, exchanges)

    Communication pipeline configuration.

        Here is the data flow diagram.  
        Data flows from parent to its immediate children.
        Children are represented by (new-line + indent) as in Python

        Notation / Key
            P = Producer
            C = Consumer
            X = eXchange (fanout)
            Q = Queue

            X(x-data-pipeline-in)
                Q(q-db-raw)
                    C(DbRawWrite, writes to TABLE_1)
                Q(q-plugins-in)
                    C(Plugin2Write, plugin_2)
                        Q(q-plugins-out)
                            X(x-decoded)
                                Q(q-plenario)
                                    C(PlenarioWrite, boto to plenario)
                                Q(q-db-decoded)
                                    C(DbDecodedWrite, writes to TABLE_2)
                Q(q-logfile)
                    C(LogfileInWrite, write raw data to logfile)
                Q(q-slack)
                    C(SlackInWrite, send messages to Slack when appropriate, eg. node comes online)
                Q(q-node-status)
                    C(NodeStatus, update the node's status based on data transmitted (eg. last_update))
