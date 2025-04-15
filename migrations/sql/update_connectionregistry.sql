DELETE FROM catalogdb.bh_connection_registry 
WHERE connection_name = 'redshift';

INSERT INTO catalogdb.bh_connection_registry (id, connection_name, connection_description,  connection_type, connection_display_name) VALUES ( 1016,'s3','Source S3 Connection','source', 'S3');
INSERT INTO catalogdb.bh_connection_registry (id, connection_name, connection_description,  connection_type, connection_display_name) VALUES ( 1017,'gcs','Source GCS Connection','source', 'GCS');