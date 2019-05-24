--
-- The measurements table contains the decomposed sensorgrams with refs back to the datagrams table
--
CREATE TABLE IF NOT EXISTS measurements (
  -- the time the measurement was taken on the node
  timestamp TIMESTAMP NOT NULL,
  -- ref to nodes table
  node_id INTEGER REFERENCES nodes (id),
  -- ref to sensors table
  sensor_id INTEGER REFERENCES sensors (id),
  -- the raw "off the serial" value of the measurement
  raw_value FLOAT NOT NULL,
  -- the computed, human accessible value of the measurement
  value FLOAT,
  -- ref to datagram this was pulled from
  datagram_id BIGINT REFERENCES datagrams (ingest_id),
  -- unique tuple
  UNIQUE (timestamp, node_id, sensor_id)
);

CREATE INDEX ON measurements (timestamp);

CREATE INDEX ON measurements (node_id);

CREATE INDEX ON measurements (sensor_id);

CREATE INDEX ON measurements (value);

--
-- Use the TimescaleDB Hypertable function to shard measurements into daily chunks for faster loading and querying
--
SELECT create_hypertable('measurements', 'timestamp', chunk_time_interval => interval '1 day');
