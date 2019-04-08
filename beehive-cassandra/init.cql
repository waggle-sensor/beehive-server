/* ANL:waggle-license
   This file is part of the Waggle Platform.  Please see the file
   LICENSE.waggle.txt for the legal details of the copyright and software
   license.  For more details on the Waggle project, visit:
            http://www.wa8.gl
   ANL:waggle-license */

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
