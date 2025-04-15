INSERT INTO bh_connection_registry (id, connection_name, connection_description,  connection_type) VALUES ( 1010,'mysql','Destination MySQL Connection','destination');
INSERT INTO bh_connection_registry (id, connection_name, connection_description,  connection_type) VALUES ( 1011,'mysql','Source MySQL Connection','source');
INSERT INTO bh_connection_registry (id, connection_name, connection_description,  connection_type) VALUES ( 1012,'oracle','Destination Oracle Connection','destination');
INSERT INTO bh_connection_registry (id, connection_name, connection_description,  connection_type) VALUES ( 1013,'oracle','Source Oracle Connection','source');
INSERT INTO bh_connection_registry (id, connection_name, connection_description,  connection_type) VALUES ( 1014,'redshift','Source Redshit Connection','source');
INSERT INTO bh_connection_registry (id, connection_name, connection_description,  connection_type) VALUES ( 1015,'redshift','Source Redshit Connection','destination');


UPDATE bh_connection_registry 
SET connection_display_name = CONCAT(UPPER(LEFT(connection_name, 1)), LOWER(SUBSTRING(connection_name, 2)));
