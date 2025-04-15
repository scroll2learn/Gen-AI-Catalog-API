INSERT INTO schema (schema_id, schema_type, commit_id, version_tag, comment, schema_path, schema_dependencies_path, platform_version) 
VALUES (2000, 'pipeline', 'pqr123', 'v1.0.0', 'Initial schema for pipelines', 'schemas/pipelines/pipeline_v1.json', 'schemas/pipelines/dependencies_v1.json', '1.0');

INSERT INTO schema (schema_id, schema_type, commit_id, version_tag, comment, schema_path, schema_dependencies_path, platform_version) 
VALUES (2001, 'pipeline', 'stu456', 'v1.1.0', 'Updated schema for pipelines', 'schemas/pipelines/pipeline_v1_1.json', 'schemas/pipelines/dependencies_v1_1.json', '1.1');

INSERT INTO schema (schema_id, schema_type, commit_id, version_tag, comment, schema_path, schema_dependencies_path, platform_version) 
VALUES (2002, 'pipeline', 'vwx789', 'v1.2.0', 'Schema for pipelines with performance improvements', 'schemas/pipelines/pipeline_v1_2.json', 'schemas/pipelines/dependencies_v1_2.json', '1.2');

INSERT INTO schema (schema_id, schema_type, commit_id, version_tag, comment, schema_path, schema_dependencies_path, platform_version) 
VALUES (2003, 'pipeline', 'yza012', 'v1.3.0', 'Revised pipeline schema for better compatibility', 'schemas/pipelines/pipeline_v1_3.json', 'schemas/pipelines/dependencies_v1_3.json', '1.3');

INSERT INTO schema (schema_id, schema_type, commit_id, version_tag, comment, schema_path, schema_dependencies_path, platform_version) 
VALUES (2004, 'pipeline', 'bcd345', 'v2.0.0', 'Major update to pipeline schema', 'schemas/pipelines/pipeline_v2.json', 'schemas/pipelines/dependencies_v2.json', '2.0');

INSERT INTO schema (schema_id, schema_type, commit_id, version_tag, comment, schema_path, schema_dependencies_path, platform_version) 
VALUES (2005, 'pipeline', 'efg678', 'v2.1.0', 'Pipeline schema with new features', 'schemas/pipelines/pipeline_v2_1.json', 'schemas/pipelines/dependencies_v2_1.json', '2.1');

INSERT INTO schema (schema_id, schema_type, commit_id, version_tag, comment, schema_path, schema_dependencies_path, platform_version) 
VALUES (2006, 'pipeline', 'hij901', 'v3.0.0', 'Complete overhaul of pipeline schema', 'schemas/pipelines/pipeline_v3.json', 'schemas/pipelines/dependencies_v3.json', '3.0');

UPDATE schema
SET is_deleted = False;

INSERT INTO bh_connection_registry (id, connection_name, connection_description,  connection_type) VALUES ( 1008,'local','Destination Local Connection','destination');
INSERT INTO bh_connection_registry (id, connection_name, connection_description,  connection_type) VALUES ( 1009,'local','Source Local Connection','source');

UPDATE bh_connection_registry
SET is_deleted = False;
