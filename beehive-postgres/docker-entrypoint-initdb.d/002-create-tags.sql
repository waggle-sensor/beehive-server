--
-- This script creates the tags table and a many to many join table
-- for nodes and tags.
--

-- Create the tags table

CREATE TABLE IF NOT EXISTS tags (
    -- auto incrementing database id
    id SERIAL PRIMARY KEY,
    -- the tag name
    name TEXT NOT NULL UNIQUE
);

-- Create the join table for nodes and tags

CREATE TABLE IF NOT EXISTS node_tags (
    -- fk reference to the nodes table
    node_id INTEGER NOT NULL REFERENCES nodes (id),
    -- fk reference to the tags table
    tag_id INTEGER NOT NULL REFERENCES tags (id),
    -- the starting date the tag is applicable to the node
    starts_on TIMESTAMP WITH TIME ZONE NOT NULL,
    -- the ending date the tag is applicable to the node
    ends_on TIMESTAMP WITH TIME ZONE
);

-- Create a funciton and trigger that enforces that a
-- node and tag pair cannot be duplicated while one has
-- a null ending date. A node can be tagged several
-- times, but only once the initial setting is closed.
-- For example, we may want to tag a node as "testing sensor x"
-- for a month. Then maybe later we want to re-add the node
-- to that group. This allows for that.

CREATE OR REPLACE FUNCTION check_node_tag_in_use()
RETURNS TRIGGER AS
$$
DECLARE
    num_rows INT;
BEGIN
    IF OLD IS NULL THEN
        RETURN NEW;
    ELSE
        num_rows := (SELECT count(*)
            FROM node_tags
            WHERE node_id = NEW.node_id
                AND tag_id = NEW.tag_id
                AND ends_on IS NULL);

        IF num_rows >= 1 THEN
            RAISE 'Node tag already in use';
        ELSE
            RETURN NEW;
        END IF;
    END IF;
END
$$
LANGUAGE 'plpgsql' IMMUTABLE;

DROP TRIGGER IF EXISTS trigger_check_node_tag_in_use ON node_tags;

CREATE TRIGGER trigger_check_node_tag_in_use
BEFORE INSERT OR UPDATE ON node_tags
FOR EACH ROW EXECUTE PROCEDURE check_node_tag_in_use();

-- Create a view for active node tags -- active being the end
-- timestamp is null or greater than right now.

DROP VIEW IF EXISTS active_node_tags;

CREATE VIEW active_node_tags AS
    SELECT *
    FROM node_tags
    WHERE ends_on IS NULL
        OR ends_on <= now();
