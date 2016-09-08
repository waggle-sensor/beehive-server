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

    P(WaggleRouter)
        X(x_data_in)
            Q(q_data_in)
                X(x_data_raw)
                    Q(q_db_raw)
                        C(Table1Write, writes to TABLE_1)
                    Q(q_decode_in)
                        C(Plugin2Write, plugin_2)
                            X(x_data_decoded)
                                Q(q_plenario_in)
                                    C(PlenarioWrite, boto to plenario)
                                Q(q_db_decoded)
                                    C(Table2Write, writes to TABLE_2)
                    Q(q_logfile)
                        C(LogfileInWrite, write raw data to logfile)
                    Q(q_slack)
                        C(SlackInWrite, send messages to Slack when appropriate, eg. node comes online)
                    Q(q_node_status)
                        C(NodeStatus, update the node's status based on data transmitted (eg. last_update))
