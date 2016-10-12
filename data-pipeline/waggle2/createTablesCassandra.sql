USE waggle;

CREATE TABLE sensor_data_raw (
    node_id         ascii,    
    date            ascii,    
    ingest_id       int,
    plugin_name     ascii,
    plugin_version  ascii,
    plugin_instance ascii,
    timestamp       TIMESTAMP,      -- milliseconds from epoch, integer
    parameter       ascii,          -- parameter name (eg. temperature, humidity)
    data            ascii,          -- data from sensor, encoded to hex
    PRIMARY KEY  ((node_id, date), plugin_name, plugin_version, plugin_instance, timestamp, parameter)
);

CREATE TABLE sensor_data_decoded (
    node_id         ascii,
    date            ascii,
    ingest_id       int,
    meta_id         int,            -- foreign key into node_meta table
    timestamp       TIMESTAMP,      -- milliseconds from epoch, integer
    data_set        ascii,          -- distinguish between identical sensors on same node
    sensor          ascii,    
    parameter       ascii,          -- parameter name (eg. temperature, humidity)
    data            ascii,          -- data from sensor, encoded to hex
    unit            ascii,
    PRIMARY KEY ((node_id, date), meta_id, sensor, parameter, timestamp, data_set, ingest_id, unit)
);

CREATE TABLE admin_messages (
    node_id         ascii,
    date            ascii,
    ingest_id       int,
    meta_id         int,            -- foreign key into node_meta table
    timestamp       TIMESTAMP,      -- milliseconds from epoch, integer
    data_set        ascii,          -- distinguish between identical sensors on same node
    sensor          ascii,    
    parameter       ascii,          -- parameter name (eg. temperature, humidity)
    data            ascii,          -- data from sensor, encoded to hex
    unit            ascii,
    PRIMARY KEY ((node_id, date), meta_id, sensor, parameter, timestamp, data_set, ingest_id, unit)
);
