--
-- This script creates the nodes table and instantiates a number of
-- functions and triggers to manage the table.
--

-- Enable extensions used by the table and its indexes. PostGIS
-- is used to create geo-spatial indexes for node locations so that
-- we can used geometric queries to look up nods. PgTrgm, or
-- Postgres Trigram, is used to build natural language indexes and
-- search capabilities so that we can search for nodes based on
-- their descriptions.

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- We want to lock down the values that are available to the op_mode
-- attribute of the nodes table.

DROP TYPE IF EXISTS OP_MODE_TYPE;

CREATE TYPE OP_MODE_TYPE AS ENUM (
    'testing',
    'storage',
    'shipped',
    'up',
    'retired',
    'lost'
);

DROP TYPE IF EXISTS NODE_TYPE_TYPE;

CREATE TYPE NODE_TYPE_TYPE AS ENUM (
    'aot',
    'ugly',
    'micro'
);

-- Create the nodes table. A note about setting the node id
-- and name as both being independently unique: we don't want
-- duplicates in here. If for whatever reason we need to change
-- the VSN for a node to one that's been taken, then we need to
-- null out the old one and then make the change.

CREATE TABLE IF NOT EXISTS nodes (
    -- auto incrementing database id
    id SERIAL PRIMARY KEY,
    -- the old node_id
    node_id TEXT NOT NULL UNIQUE,
    -- the old vsn: any friendly name
    name TEXT UNIQUE,
    -- the date the name was added to the node
    name_timestamp TIMESTAMP WITH TIME ZONE,
    -- the operational mode of the node
    op_mode OP_MODE_TYPE NOT NULL DEFAULT 'testing',
    -- modem id
    modem_imei TEXT UNIQUE,
    -- sim card id
    sim_iccid TEXT UNIQUE,
    -- reverse ssh tunnel port number
    rssh_port INTEGER UNIQUE,
    -- base location lat coordinate
    latitude FLOAT,
    -- base location lon coordinate
    longitude FLOAT,
    -- base location
    location GEOMETRY,
    -- base elevation
    elevation FLOAT,
    -- human readable address or location
    address TEXT,
    -- generic descriptive information
    description TEXT,
    -- what type of node is this
    node_type NODE_TYPE_TYPE NOT NULL DEFAULT 'aot',
    -- what version of the hardware is this build
    hardware_version TEXT,
    -- what sensors are on board
    sensor_config TEXT,
    -- what software version is the node controller running
    nc_build_version TEXT,
    -- what software version is the edge processor running
    ep_build_version TEXT,
    -- what software version is the wagman running
    wgn_build_version TEXT,
    -- what software version is the coresens board running
    cs_build_version TEXT,
    -- initial build token generated for node by beehive
    token TEXT
);

-- Set up the indexes for the table

CREATE INDEX ON nodes USING gist(location);

CREATE INDEX ON nodes USING gin(to_tsvector('english', address));

CREATE INDEX ON nodes USING gin(to_tsvector('english', description));

CREATE INDEX ON nodes (node_type);

-- Create a function and trigger to set the location geom if the lat and lon are set

CREATE OR REPLACE FUNCTION set_node_location()
RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
        NEW.location = ST_MakePoint(NEW.longitude, NEW.latitude);
    ELSE
        NEW.location = NULL;
    END IF;

    RETURN NEW;
END
$$
LANGUAGE 'plpgsql' IMMUTABLE;

DROP TRIGGER IF EXISTS tgr_set_node_location ON nodes;

CREATE TRIGGER tgr_set_node_location
BEFORE INSERT OR UPDATE ON nodes
FOR EACH ROW EXECUTE PROCEDURE set_node_location();

-- Create a trigger that will apply the current timestamp when the name is set on the node

CREATE OR REPLACE FUNCTION set_node_name_timestamp()
RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.name IS NOT NULL THEN
        NEW.name_timestamp = now();
    END IF;

    RETURN NEW;
END
$$
LANGUAGE 'plpgsql' IMMUTABLE;

DROP TRIGGER IF EXISTS tgr_set_node_name_timestamp ON nodes;

CREATE TRIGGER tgr_set_node_name_timestamp
BEFORE INSERT OR UPDATE ON nodes
FOR EACH ROW EXECUTE PROCEDURE set_node_name_timestamp();

-- Create a convenience function to find the next available rssh port for a new node

CREATE OR REPLACE FUNCTION get_next_available_node_rssh_port()
RETURNS INTEGER AS
$$
DECLARE
    max_port INT;
BEGIN
    max_port := (SELECT max(rssh_port) FROM nodes);
    IF max_port IS NOT NULL THEN
        RETURN max_port + 1;
    ELSE
        RETURN 5000;
    END IF;
END
$$
LANGUAGE 'plpgsql' IMMUTABLE;

-- Seup a table that logs all changes to the nodes table along with
-- triggers that capture every write/delete action.

CREATE TABLE IF NOT EXISTS node_changes (
    node_id TEXT,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    query TEXT NOT NULL,
    action TEXT NOT NULL,
    old_row JSONB,
    new_row JSONB
);

CREATE OR REPLACE FUNCTION audit_nodes()
RETURNS TRIGGER AS
$$
DECLARE
    node_id TEXT;
    audit_row node_changes;
BEGIN
    IF TG_WHEN <> 'AFTER' THEN
        RAISE EXCEPTION 'audit_nodes() may only run as an AFTER trigger';
    END IF;

    IF OLD.node_id IS NOT NULL THEN
        node_id = OLD.node_id;
    ELSE
        node_id = NEW.node_id;
    END IF;

    audit_row = ROW(
        node_id,          -- node_id
        now(),            -- timestamp
        current_query(),  -- query
        TG_OP,            -- action (INSERT, UPDATE, DELETE, TRUCATE)
        null,             -- old_row
        null              -- new_row
    );

    IF OLD IS NOT NULL THEN
        audit_row.old_row = to_jsonb(OLD.*);
    END IF;

    IF TG_OP IN ('INSERT', 'UPDATE') THEN
        audit_row.new_row = to_jsonb(NEW.*);
    END IF;

    INSERT INTO node_changes VALUES (audit_row.*);
    RETURN NULL;
END
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS tgr_audit_nodes_row ON nodes;

CREATE TRIGGER tgr_audit_nodes_row
AFTER INSERT OR UPDATE OR DELETE ON nodes
FOR EACH ROW EXECUTE PROCEDURE audit_nodes();

DROP TRIGGER IF EXISTS tgr_audit_nodes_stm ON nodes;

CREATE TRIGGER tgr_audit_nodes_stm
AFTER TRUNCATE ON nodes
FOR EACH STATEMENT EXECUTE PROCEDURE audit_nodes();
