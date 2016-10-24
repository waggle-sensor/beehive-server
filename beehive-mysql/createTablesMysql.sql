CREATE DATABASE IF NOT EXISTS waggle;

USE waggle;

# data that has 1 value at a time per node_id
CREATE TABLE node_management (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    node_id             VARCHAR(32),
    rssh_port           INT,
    rssh_key            TEXT,
    cert                TEXT,
    sim_iccid           VARCHAR(64),  # 3G/4G
    modem_imei          VARCHAR(64),  # modem
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
ALTER TABLE node_management ADD INDEX idx_node (node_id);

CREATE TABLE calibration (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    part_number         TEXT,
    mac_address         TEXT,
    time_started        TIMESTAMP,
    calib               JSON,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE node_config (
    node_config_id          INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name                    TEXT,
    node_id                 VARCHAR(32),
    time_started            TIMESTAMP,
    street_address          TEXT,
    location_lat            FLOAT,
    location_long           FLOAT,
    location_altitude       FLOAT,
    location_elevation      FLOAT,    # centimeters above ground
    location_orientation    FLOAT,    # relative to true North, degrees cw ???
    config                  JSON,    # hardware, software, and relationships
    time_created            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
ALTER TABLE node_config ADD INDEX idx_node_time (node_id, time_started);


CREATE TABLE node_meta (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    config_id           INT NOT NULL,
    calibration_ids     JSON DEFAULT NULL,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE node_notes (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    node_id             INT,
    note                TEXT,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
ALTER TABLE node_notes ADD INDEX idx_node (node_id);

CREATE TABLE hardware (
    id                  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vendor              TEXT,
    part_number         TEXT,
    version             TEXT,
    datasheet_url       TEXT,
    metadata            JSON,
    time_created        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_last_updated   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE software (
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


