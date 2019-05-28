--
-- Sensors are the things that capture measurements.
--
CREATE TABLE IF NOT EXISTS sensors (
  -- auto incrementing database id
  id SERIAL PRIMARY KEY,
  -- the hex keys used to identify the sensor in sensorgrams
  packet_sensor_id TEXT NOT NULL,
  packet_parameter_id TEXT NOT NULL,
  -- the name of the sensor
  sensor TEXT NOT NULL,
  -- what the sensor captures
  parameter TEXT NOT NULL,
  -- unit of measurement
  uom TEXT NOT NULL,
  -- the typical minimum value of the captured measurement
  min FLOAT,
  -- the typical maximum value of the captured measurement
  max FLOAT,
  -- the url to the sensor's data sheet
  data_sheet TEXT,
  -- explicitly unique tuple to id the sensor in packets
  UNIQUE (packet_sensor_id, packet_parameter_id),
  -- explicitly unique tuple to name the node
  UNIQUE (subsystem, sensor, parameter)
);

CREATE INDEX ON sensors (subsystem);

CREATE INDEX ON sensors (sensor);

CREATE INDEX ON sensors (parameter);

CREATE INDEX ON sensors USING gin(to_tsvector('english', ontology));

--
--
--
CREATE TABLE IF NOT EXISTS plugin_sensors (
  -- ref to plugins table
  plugin_id INTEGER REFERENCES plugins (id),
  -- ref to sensors table
  sensor_id INTEGER REFERENCES sensors (id),
  -- a hierarchical text description of the sensor
  ontology TEXT NOT NULL,
  -- the major hardware system the sensor is part of
  subsystem TEXT NOT NULL,
  -- unique tuple of plugin and sensor
  UNIQUE (plugin_id, sensor_id)
);
