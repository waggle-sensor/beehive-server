--
-- This script creates the sensors and plugins tables. Sensors and plugins
-- work together to qualify what kinds of measurements are recorded.
--

-- Ensure that we're working with the right database.

CREATE DATABASE IF NOT EXISTS waggle;
\c waggle

-- Create the sensors table. The values in this table are the
-- singular sensor definitions. For instantiated sensors, you'll
-- need to know the plugin that recorded the measurements to
-- pull its ontology and subsystem.

CREATE TABLE IF NOT EXISTS sensors (
    -- auto incrementing database id
    id SERIAL PRIMARY KEY,
    -- hex value used to id sensor in waggle packets
    packet_sensor_id TEXT NOT NULL,
    -- hex value used to id param in waggle packets
    packet_parameter_id TEXT NOT NULL,
    -- the name of the sensor (usually a chip name, but not always)
    sensor TEXT NOT NULL,
    -- the name of the parameter (the thing being measured)
    parameter TEXT NOT NULL,
    -- unit of measurement
    uom TEXT,
    -- minimum "good" value
    min FLOAT,
    -- maximum "good" value
    max FLOAT,
    -- link to the sensor data sheet
    data_sheet TEXT,
    -- explicit unique tuple for the packet ids
    UNIQUE (packet_sensor_id, packet_parameter_id),
    -- explicit unique tuple of sensor and param
    UNIQUE (sensor, parameter)
);


-- Create the plugins table. This table tracks the various
-- plugins that we use. This table is used in conjunction with
-- the sensors table to give further context to the final
-- sensor information available in measurements -- i.e. their
-- subsystem and ontology.

CREATE TABLE IF NOT EXISTS plugins (
    -- auto incrementing database id
    id SERIAL PRIMARY KEY,
    -- value used to id plugin in waggle packets
    packet_plugin_id TEXT NOT NULL,
    -- the name of the plugin
    name TEXT NOT NULL,
    -- the version string of the plugin
    version TEXT NOT NULL,
    -- explicit unique tuple of packet id and version
    UNIQUE (packet_plugin_id, version),
    -- explicit unique tuple of name and version
    UNIQUE (name, version)
);


-- Create the join table for plugins and sensors: this is where
-- ontologies and subsystems are named.

CREATE TABLE IF NOT EXISTS plugins_sensors (
    -- fk to the plugins table
    plugin_id INTEGER NOT NULL REFERENCES plugins (id),
    -- fk to the sensors table
    sensor_id INTEGER NOT NULL REFERENCES sensors (id),
    -- the subsystem name to apply to the plugin/sensor pair
    subsystem TEXT NOT NULL,
    -- a hierarchical tagging system for the sensor's measurement
    ontology TEXT NOT NULL,
    -- explicit unique tuple of plugin and sensor
    UNIQUE (plugin_id, sensor_id)
);
