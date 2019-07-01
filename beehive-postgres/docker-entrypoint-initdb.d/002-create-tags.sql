--
-- This script creates the tags table and a many to many join table
-- for nodes and tags.
--

-- Ensure that we're working with the right database.

CREATE DATABASE IF NOT EXISTS waggle;
\c waggle

-- Create the tags table

CREATE TABLE IF NOT EXISTS tags (
    -- auto incrementing database id
    id SERIAL PRIMARY KEY,
    -- the tag name
    name TEXT NOT NULL UNIQUE,
    -- is this tag used to export data sets?
    export BOOLEAN DEFAULT FALSE
);

-- Create the join table for nodes and tags

CREATE TABLE IF NOT EXISTS node_tags (
    node_id INTEGER NOT NULL REFERENCES nodes (id),
    tag_id INTEGER NOT NULL REFERENCES tags (id),
    UNIQUE (node_id, tag_id)
);
