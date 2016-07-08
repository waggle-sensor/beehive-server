
use waggle;

CREATE TABLE users (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username            VARCHAR(64) NOT NULL UNIQUE,
    password            VARCHAR(64),
    real_name           VARCHAR(64),
    email               VARCHAR(64),
    address             VARCHAR(64),
    city                VARCHAR(32),
    postal_code         VARCHAR(10),
    country             VARCHAR(15),
    admin               BOOLEAN NOT NULL DEFAULT 0
);

ALTER TABLE users ADD INDEX (username);


CREATE TABLE projects (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(60),
    owner               INT,
    public              BOOLEAN NOT NULL DEFAULT 0,
    ext_link            VARCHAR(256)
);
ALTER TABLE projects ADD INDEX (owner);

CREATE TABLE nodes (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    node_id             VARCHAR(16),
    hostname            VARCHAR(64),
    project             INT,
    description         VARCHAR(255),
    reverse_ssh_port    MEDIUMINT,
    hardware            JSON
);
ALTER TABLE nodes ADD INDEX (project);

