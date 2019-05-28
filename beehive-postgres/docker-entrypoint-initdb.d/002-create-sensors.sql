--
-- Sensors are the things that capture measurements.
--
CREATE TABLE IF NOT EXISTS sensors (
  -- auto incrementing database id
  id SERIAL PRIMARY KEY,
  -- the hex keys used to identify the sensor in sensorgrams
  packet_sensor_id TEXT NOT NULL,
  packet_parameter_id TEXT NOT NULL,
  -- the name of the sensor
  sensor TEXT NOT NULL,
  -- what the sensor captures
  parameter TEXT NOT NULL,
  -- unit of measurement
  uom TEXT NOT NULL,
  -- the typical minimum value of the captured measurement
  min FLOAT,
  -- the typical maximum value of the captured measurement
  max FLOAT,
  -- the url to the sensor's data sheet
  data_sheet TEXT,
  -- explicitly unique tuple to id the sensor in packets
  UNIQUE (packet_sensor_id, packet_parameter_id),
  -- explicit unique tuple to keep names clean
  UNIQUE (sensor, parameter)
);
