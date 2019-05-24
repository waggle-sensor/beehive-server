--
-- The datagrams table stores the raw datagram information.
--
CREATE TABLE IF NOT EXISTS datagrams (
  -- auto incrementing primary key
  id BIGSERIAL PRIMARY KEY,
  -- the time the waggle packet was ingested; pulled from msg headers
  timestamp TIMESTAMP NOT NULL,
  -- ref to nodes table; pulled from msg headers
  node_id INTEGER REFERENCES nodes (id),
  -- ref to plugins table; pulled from msg body tuple (name, version)
  plugin_id INTEGER REFERENCES plugins (id),
  -- the instance of the plugin that created the datagram; pulled from msg body
  plugin_instance TEXT NOT NULL,
  -- the sensorgram data embedded in the message body; this contains the measurements
  sensorgrams BYTEA NOT NULL,
  -- set a unique constraint for the header and first level fields
  UNIQUE (timestamp, node_id, plugin_name, plugin_version, plugin_instance, parameter)
);

--
-- Use the TimescaleDB Hypertable function to shard datagrams into daily chunks for faster loading and processing
--
SELECT create_hypertable('datagrams', 'timestamp', chunk_time_interval => interval '1 day');
