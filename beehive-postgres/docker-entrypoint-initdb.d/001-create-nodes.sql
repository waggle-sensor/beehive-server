--
-- The nodes table tracks the identifiers and general information about nodes.
--
CREATE TABLE IF NOT EXISTS nodes (
  -- auto increment database id
  id SERIAL PRIMARY KEY,
  -- the internal identifier of the nodes; for waggle people
  node_id TEXT NOT NULL UNIQUE,
  -- the public identifier of the nodes; for regular people
  vsn TEXT NOT NULL UNIQUE,
  -- the node's location's lat coordinate
  latitude FLOAT,
  -- the node's location's lon coordinate
  longitude FLOAT,
  -- the node's location stored as a geometric point
  location GEOMETRY,
  -- the human readable address of the node
  address TEXT,
  -- any additional descriptive information about the node
  description TEXT,
  -- the date the node went into production service
  commissioned_on TIMESTAMP,
  -- the date the node was taken out of production service
  decommissioned_on TIMESTAMP
);

CREATE INDEX ON nodes (node_id);

CREATE INDEX ON nodes (vsn);

CREATE INDEX ON nodes USING gist(location) ;

CREATE INDEX ON nodes USING gin(to_tsvector('english', address));

CREATE INDEX ON nodes USING gin(to_tsvector('english', description));

--
-- This function converts the float lon/lat into a PostGIS location
--
CREATE OR REPLACE FUNCTION set_node_location ()
RETURNS TRIGGER AS 
$$
BEGIN
  IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
    NEW.location = ST_MakePoint(NEW.longitude, NEW.latitude);
  END IF;

  RETURN NEW;
END
$$ LANGUAGE 'plpgsql' IMMUTABLE;

--
-- This sets up the trigger to automatically create the location for a node if the lon/lat are set.
--
DROP TRIGGER IF EXISTS trigger_set_node_location ON nodes;

CREATE TRIGGER trigger_set_node_location
  BEFORE INSERT OR UPDATE ON nodes
  FOR EACH ROW
  EXECUTE PROCEDURE set_node_location();
