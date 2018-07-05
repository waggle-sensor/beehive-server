CREATE KEYSPACE IF NOT EXISTS waggle
  WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2 };

USE waggle;

CREATE TABLE IF NOT EXISTS sensor_data_raw (
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
