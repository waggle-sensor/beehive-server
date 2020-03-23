-- ANL:waggle-license
--  This file is part of the Waggle Platform.  Please see the file
--  LICENSE.waggle.txt for the legal details of the copyright and software
--  license.  For more details on the Waggle project, visit:
--           http://www.wa8.gl
-- ANL:waggle-license

SET GLOBAL default_password_lifetime = 0;

CREATE DATABASE IF NOT EXISTS waggle;

USE waggle;


# data that has 1-to-1 mapping with node_id
CREATE TABLE IF NOT EXISTS waggle.node_management (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    node_id             VARCHAR(32),
    rssh_port           INT,
    rssh_key            TEXT,   # RSA private key, from key.pem
    rssh_cert           TEXT,   # x509 cert (part of which is an RSA public key), from cert.pem
    sim_iccid           VARCHAR(64),  # 3G/4G
    modem_imei          VARCHAR(64),  # modem
    opmode              VARCHAR(64) DEFAULT 'testing',
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_node (node_id)
);

CREATE TABLE IF NOT EXISTS waggle.calibration (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    part_number         TEXT,
    mac_address         TEXT,
    time_started        TIMESTAMP,
    calib               JSON,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS waggle.node_config (
    node_config_id          INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name                    TEXT,
    description             TEXT,           # description of the node might change eg. if it moves
    node_id                 VARCHAR(32),
    time_started            TIMESTAMP,      # the time this config started - went into effect
    street_address          TEXT,
    location_lat            FLOAT,
    location_long           FLOAT,
    location_altitude       FLOAT,
    location_elevation      FLOAT,  # centimeters above ground
    location_orientation    FLOAT,  # relative to true North, degrees cw ???
    config                  JSON,   # hardware, software, and relationships
    time_created            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX   idx_node_time (node_id, time_started)
);


CREATE TABLE IF NOT EXISTS waggle.node_meta (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    config_id           INT NOT NULL,
    calibration_ids     JSON DEFAULT NULL,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS waggle.node_notes (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    node_id             INT,
    note                TEXT,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_node (node_id)
);

CREATE TABLE IF NOT EXISTS waggle.hardware (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vendor              TEXT,
    part_number         TEXT,
    version             TEXT,
    datasheet_url       TEXT,
    metadata            JSON,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS waggle.software (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name                TEXT,
    description         TEXT,
    version             TEXT,
    source_code_url     TEXT,
    documentation_url   TEXT,
    metadata            JSON,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS waggle.node_offline (
  node_id               VARCHAR(16) NOT NULL,
  start_time            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS waggle.registration_keys (
    id int auto_increment PRIMARY KEY, 
    batchName TEXT,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN not null default 1,   # Usually a key is not active anymore when it has been used. You can also actively disable a key using this flag even if it has not been used yet.
    used BOOLEAN not null default 0,     # "used" means that a node used the registration_key. A used node should not active.
    used_date TIMESTAMP NULL DEFAULT NULL,

    rsa_private_key              TEXT,   # RSA private key, from key.pem
    rsa_public_key               TEXT,
    signed_client_certificate    TEXT   # x509 cert (part of which is an RSA public key), from cert.pem
);




CREATE TABLE IF NOT EXISTS waggle.credentials (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    node_id             VARCHAR(16),
   
    rsa_private_key              TEXT,   # RSA private key, from key.pem
    rsa_public_key               TEXT,
    signed_client_certificate    TEXT   # x509 cert (part of which is an RSA public key), from cert.pem

);

CREATE TABLE IF NOT EXISTS waggle.nodes (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    node_id             VARCHAR(16),
    hostname            VARCHAR(64),
    project             INT,
    description         VARCHAR(255),
    reverse_ssh_port    MEDIUMINT,
    hardware            JSON,
    name                VARCHAR(64),
    location            VARCHAR(255),
    opmode              VARCHAR(64) DEFAULT 'testing',
    last_updated        TIMESTAMP
);
