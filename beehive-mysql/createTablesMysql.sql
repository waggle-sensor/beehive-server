CREATE DATABASE IF NOT EXISTS waggle;

USE waggle;

# data that has 1-to-1 mapping with node_id
CREATE TABLE IF NOT EXISTS node_management (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    node_id             VARCHAR(32),
    rssh_port           INT,
    rssh_key            TEXT,   # RSA private key, from key.pem
    rssh_cert           TEXT,   # x509 cert (part of which is an RSA public key), from cert.pem
    sim_iccid           VARCHAR(64),  # 3G/4G
    modem_imei          VARCHAR(64),  # modem
    opmode              VARCHAR(64) DEFAULT 'testing',
    groups              VARCHAR(128) DEFAULT '',
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_node (node_id)
);

# decoded sensor data, from Cassanrda
CREATE TABLE IF NOT EXISTS sensor_data_decoded (
    node_id         VARCHAR(16),
    date            VARCHAR(16),
    ingest_id       INT,
    meta_id         INT,            # foreign key into node_meta table
    timestamp       TIMESTAMP,      # milliseconds from epoch, integer
    data_set        VARCHAR(64),    # distinguish between identical sensors on same node
    sensor          VARCHAR(64),    # eg. TMP112
    parameter       VARCHAR(64),    # parameter name (eg. temperature, humidity)
    data            TEXT,           # data from sensor, decoded / human-readable
    unit            VARCHAR(64),
    PRIMARY KEY(node_id)
);


CREATE TABLE IF NOT EXISTS calibration (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    part_number         TEXT,
    mac_address         TEXT,
    time_started        TIMESTAMP,
    calib               JSON,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS node_config (
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


CREATE TABLE IF NOT EXISTS node_meta (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    config_id           INT NOT NULL,
    calibration_ids     JSON DEFAULT NULL,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS node_notes (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    node_id             INT,
    note                TEXT,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_node (node_id)
);

CREATE TABLE IF NOT EXISTS hardware (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vendor              TEXT,
    part_number         TEXT,
    version             TEXT,
    datasheet_url       TEXT,
    metadata            JSON,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS software (
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

CREATE TABLE IF NOT EXISTS node_offline (
  node_id               VARCHAR(16) NOT NULL,
  start_time            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

#################################################################################
#####  SOON TO BE DEPRECATED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#################################################################################
CREATE TABLE IF NOT EXISTS nodes (
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
    groups              VARCHAR(128) DEFAULT '',
    last_updated        TIMESTAMP
);
