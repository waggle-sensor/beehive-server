--
-- This table holds metadata for plugins
--
CREATE TABLE IF NOT EXISTS plugins (
  -- auto incrementing database id
  id SERIAL PRIMARY KEY,
  -- the id used in the packets -- a stand in for the name
  packet_id TEXT NOT NULL UNIQUE,
  -- the name of the plugin
  name TEXT NOT NULL,
  -- the version of the plugin
  version TEXT NOT NULL,
  -- unique tuple
  UNIQUE (name, version)
);

--
-- This table joins sensors to plugins to define subsystems and ontologies.
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
