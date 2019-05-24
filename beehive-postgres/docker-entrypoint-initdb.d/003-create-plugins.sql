--
-- This table holds metadata for plugins
--
CREATE TABLE IF NOT EXISTS plugins (
  -- auto incrementing database id
  id SERIAL PRIMARY KEY,
  -- the name of the plugin
  name TEXT NOT NULL,
  -- the version of the plugin
  version TEXT NOT NULL,
  -- unique tuple
  UNIQUE (name, version)
);
