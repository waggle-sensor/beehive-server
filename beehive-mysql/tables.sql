
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
    admin               BOOLEAN NOT NULL DEFAULT 0,
    token               VARCHAR(36)
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
    hardware            JSON,
    name                VARCHAR(64),
    location            VARCHAR(255),
    opmode              VARCHAR(64) DEFAULT 'inactive',
    last_updated        TIMESTAMP
);
ALTER TABLE nodes ADD INDEX (project);

CREATE TABLE roles (
    role_id                       INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    role_name                     VARCHAR(50),
    permission_admin              BOOLEAN NOT NULL DEFAULT FALSE,
    permission_project_admin      BOOLEAN NOT NULL DEFAULT FALSE,
    permission_project_read       BOOLEAN NOT NULL DEFAULT FALSE,
    permission_node_admin         BOOLEAN NOT NULL DEFAULT FALSE,
    permission_node_read          BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO roles VALUES ( 1, "admin",          TRUE,  TRUE,  TRUE,  TRUE,  TRUE);
INSERT INTO roles VALUES ( 2, "project-admin",  FALSE, TRUE,  TRUE,  TRUE,  TRUE);
INSERT INTO roles VALUES ( 3, "project-user",   FALSE, FALSE, TRUE,  TRUE,  TRUE);
INSERT INTO roles VALUES ( 4, "node-admin",     FALSE, FALSE, FALSE, TRUE,  TRUE);
INSERT INTO roles VALUES ( 5, "node-user",      FALSE, FALSE, FALSE, FALSE, TRUE);
INSERT INTO roles VALUES ( 6, "guest",          FALSE, FALSE, FALSE, FALSE, FALSE);


CREATE TABLE projects_access_control (
    project            INT,
    user	        INT,
    role_id            INT,   
    UNIQUE KEY (project, user)
);
