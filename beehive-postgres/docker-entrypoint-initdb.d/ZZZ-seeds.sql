
INSERT INTO nodes (node_id, vsn)
    VALUES ('0000000000000001', '001');

INSERT INTO plugins (id, packet_id, version, name)
    VALUES (9999, '1', '0.0.1', 'TestSense');

INSERT INTO sensors (id, packet_sensor_id, packet_parameter_id, sensor, parameter, uom)
    VALUES (9999, '1', '1', 'uptime', 'uptime', 'seconds');

INSERT INTO plugins_sensors (plugin_id, sensor_id, ontology, subsystem)
    VALUES (9999, 9999, '/system/uptime', 'nc');
