--
-- This script creates the nodes table and instantiates a number of
-- functions and triggers to manage the table.
--

-- Ensure that we're working with the right database.

CREATE DATABASE IF NOT EXISTS waggle;
\c waggle

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

CREATE TYPE IF NOT EXISTS OP_MODE AS ENUM (
    'testing',
    'storage',
    'shipped',
    'up',
    'retired',
    'lost'
);

-- Create the nodes table

CREATE TABLE IF NOT EXISTS nodes (
    -- auto incrementing database id
    id SERIAL PRIMARY KEY,
    -- the old node_id
    node_id TEXT UNIQUE,
    -- the old vsn: any friendly name
    name TEXT UNIQUE,
    -- the operational mode of the node
    op_mode OP_MODE DEFAULT 'testing',
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
    description TEXT
);

-- Set up the indexes for the table

CREATE INDEX IF NOT EXISTS ON nodes USING gist(location);

CREATE INDEX IF NOT EXISTS ON nodes USING gin(to_tsvector('english', address));

CREATE INDEX IF NOT EXISTS ON nodes USING gin(to_tsvector('english', description));

-- Turn on audit logging for the table

SELECT audit.audit_table('nodes');

-- Create a function and trigger to set the location geom if the lat and lon are set

CREATE OR REPLACE FUNCTION set_node_location()
RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
        NEW.location = ST_MakePoint(NEW.longitude, NEW.latitude);
    END IF;

    RETURN NEW;
END
$$
LANGUAGE 'plpgsql' IMMUTABLE;

DROP TRIGGER IF EXISTS trigger_set_node_location ON nodes;

CREATE TRIGGER trigger_set_node_location
    BEFORE INSERT OR UPDATE ON nodes
    FOR EACH ROW
    EXECUTE PROCEDURE set_node_location();

-- Create a convenience function to find the next available rssh port for a new node

CREATE OR REPLACE FUNCTION get_next_available_node_rssh_port()
RETURNS INTEGER AS
$$
DECLARE
    max_port INTEGER
BEGIN
    max_port := SELECT max(rssh_port) FROM nodes;
    IF max_port IS NOT NULL THEN
        RETURN max_port + 1;
    ELSE
        RETURN 5000;
    END IF;
END
$$
LANGUAGE 'plpgsql' IMMUTABLE;
