USE waggle;

CREATE TABLE sensor_data_raw (
    node_id         ascii,    
    date            ascii,    
    ingest_id       int,
    plugin_name     ascii,
    plugin_version  ascii,
    plugin_instance ascii,
    time_stamp      TIMESTAMP,      -- seconds from epoch
    parameter       ascii,          -- parameter name (eg. temperature, humidity)
    data            ascii,          -- data from sensor, encoded to hex
    PRIMARY KEY (node_id, date)
);

CREATE TABLE sensor_data_decoded (
    node_id         ascii,
    date            ascii,
    ingest_id       int,
    data_set        ascii,          -- distinguish between identical sensors on same node
    time_stamp      TIMESTAMP,      -- microseconds from epoch
    sensor          ascii,    
    parameter       ascii,          -- parameter name (eg. temperature, humidity)
    unit            ascii,
    data            ascii,          -- data from sensor, encoded to hex
    data_meta_id    int,            -- foreign key into node_meta table
    PRIMARY KEY (node_id, date)
);

CREATE TABLE admin_messages (
    node_id         ascii,
    date            ascii,
    ingest_id       int,
    data_set        ascii,          -- distinguish between identical sensors on same node
    time_stamp      TIMESTAMP,      -- microseconds from epoch
    sensor          ascii,    
    parameter       ascii,          -- parameter name (eg. temperature, humidity)
    unit            ascii,
    data            ascii,          -- data from sensor, encoded to hex
    data_meta_id    int,            -- foreign key into node_meta table
    PRIMARY KEY (node_id, date)
);
