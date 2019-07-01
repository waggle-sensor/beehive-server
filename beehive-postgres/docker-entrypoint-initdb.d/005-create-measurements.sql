--
-- This script creates the measurements table and shards it based on timestamp
-- using the timescaledb extension.
--

-- Ensure that we're working with the right database.

CREATE DATABASE IF NOT EXISTS waggle;
\c waggle

-- Enable the timescaledb extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- The measurements table contains the decomposed sensorgrams with refs back to the datagrams table

CREATE TABLE IF NOT EXISTS measurements (
    -- the time the measurement was taken on the node
    timestamp TIMESTAMP NOT NULL,
    -- ref to nodes table
    node_id INTEGER NOT NULL REFERENCES nodes (id),
    -- ref to sensors table
    sensor_id INTEGER NOT NULL REFERENCES sensors (id),
    -- ref to plugins table
    plugin_id INTEGER NOT NULL REFERENCES plugins (id),
    -- the raw "off the serial" value of the measurement
    raw_value TEXT NOT NULL,
    -- the computed, human accessible value of the measurement
    value TEXT
);

--
-- Use the TimescaleDB Hypertable function to shard measurements into daily chunks for faster loading and querying
--
SELECT create_hypertable('measurements', 'timestamp', chunk_time_interval => interval '1 day');

--
-- Add indexes
--
ALTER TABLE measurements ADD UNIQUE (timestamp, node_id, sensor_id, plugin_id);

CREATE INDEX ON measurements (timestamp);

CREATE INDEX ON measurements (node_id);

CREATE INDEX ON measurements (sensor_id);

CREATE INDEX ON measurements (plugin_id);
