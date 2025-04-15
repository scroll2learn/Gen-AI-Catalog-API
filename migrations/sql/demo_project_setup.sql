INSERT INTO bh_project (access_details, tags, bh_project_id, bh_project_cld_id, bh_project_name, bh_project_desc, cloud_provider_cd, cloud_region_cd, access_type_cd, validation_status, business_url, lake_name, lake_desc, env_cd, status_cd) VALUES ('{"key":"value"}', '{"key":"value"}', 1, 'demo-project-123', 'demo-project', 'This is demo project', 101, 2, 201, True, 'http://www.demo-project.com', 'demo-lake', 'This is demo lake', 301, 601);

INSERT INTO lake_zone (lake_zone_id, lake_zone_cd, lake_zone_url, lake_zone_std_days, lake_zone_arch_days, bh_project_id) VALUES (1, 401, 's3://demolake.d.b.xyz12.demo-project.com', 60, 365, 1);
INSERT INTO lake_zone (lake_zone_id, lake_zone_cd, lake_zone_url, lake_zone_std_days, lake_zone_arch_days, bh_project_id) VALUES (2, 402, 's3://demolake.d.s.xyz12.demo-project.com', 60, 365, 1);
INSERT INTO lake_zone (lake_zone_id, lake_zone_cd, lake_zone_url, lake_zone_std_days, lake_zone_arch_days, bh_project_id) VALUES (3, 403, 's3://demolake.d.g.xyz12.demo-project.com', 60, 365, 1);
INSERT INTO lake_zone (lake_zone_id, lake_zone_cd, lake_zone_url, lake_zone_std_days, lake_zone_arch_days, bh_project_id) VALUES (4, 404, 's3://demolake.d.l.xyz12.demo-project.com', 60, 365, 1);
INSERT INTO lake_zone (lake_zone_id, lake_zone_cd, lake_zone_url, lake_zone_std_days, lake_zone_arch_days, bh_project_id) VALUES (5, 405, 's3://demolake.d.q.xyz12.demo-project.com', 60, 365, 1);

INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"Electrical", "key": "Vehicle"}', 1, 'Electric Vehicle', 'Electric Vehicle Population Data', '2024-06-10 14:25:15', '0%', 701, 1, 'electric_vehicle_population_data');

INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (1, 'EV Owner', 'Demo User', 999, 999, 1, 'evowner');

INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory) VALUES (1, 'Demo Layout', 1501, 1601, null, True, 1701, 1801, 1905, '.*\.csv$', True, 1, 'demolayout', 2001, true);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key) VALUES ('{"key":"value"}', 1, 'Employe Id', 'Employe Data', 1, True, 0, 0, 1201, 1, 'employeid');
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key) VALUES ('{"key":"value"}', 2, 'Employe Name', 'Employe Data', 2, False, 0, 20, 1202, 1, 'employename');
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key) VALUES ('{"key":"value"}', 3, 'Employe Salary', 'Employe Data', 3, False, 0, 0, 1201, 1, 'employesalary');
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key) VALUES ('{"key":"value"}', 4, 'Employe Dept', 'Employe Data', 4, False, 0, 10, 1202, 1, 'employedept');
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key) VALUES ('{"key":"value"}', 5, 'Employe Joining Date', 'Employe Data', 5, False, 0, 0, 1204, 1, 'employejoiningdate');

INSERT INTO layout_fields_dq (fld_dq_params, fld_dq_id, fld_dq_level, lyt_fld_id, fld_dq_type_id) VALUES ('{"rule_expr": "length(employename) <= 10"}', 1, 'ERROR', 2, 2);
INSERT INTO layout_fields_dq (fld_dq_params, fld_dq_id, fld_dq_level, lyt_fld_id, fld_dq_type_id) VALUES ('{"date_pattern": "YYYY-MM-DDTHH:MM:SS"}', 2, 'ERROR', 5, 4);
INSERT INTO layout_fields_dq (fld_dq_params, fld_dq_id, fld_dq_level, lyt_fld_id, fld_dq_type_id) VALUES ('{"rule_expr": "employe_id IS NOT NULL"}', 3, 'ERROR', 1, 6);
INSERT INTO layout_fields_dq (fld_dq_params, fld_dq_id, fld_dq_level, lyt_fld_id, fld_dq_type_id) VALUES ('{"rule_expr": "employedept IN ([1, 2, 3, 4])"}', 4, 'ERROR', 4, 7);

INSERT INTO pipelines (tags, pipeline_schedule, pipeline_id, pipeline_name, pipeline_key, pipeline_desc, pipeline_type_cd, pipeline_zone_type_cd) VALUES ('{"key":"value"}', '{"schedule": ""}', 1, 'Demo Pipeline', 'demopipeline', 'This is Demo Pipeline', 1401, 401);
INSERT INTO pipeline_sources (pipeline_src_id, pipeline_id, data_src_id, data_src_lyt_id, pipeline_src_order) VALUES (1, 1, 1, 1, 1);
-- Update sequences of above tables
SELECT setval('bh_project_bh_project_id_seq', 2, false);
SELECT setval('lake_zone_lake_zone_id_seq', 6, false);
SELECT setval('data_source_data_src_id_seq', 2, false);
SELECT setval('data_source_metadata_data_src_mtd_id_seq', 2, false);
SELECT setval('data_source_layout_data_src_lyt_id_seq', 2, false);
SELECT setval('layout_fields_lyt_fld_id_seq', 6, false);
SELECT setval('layout_fields_dq_fld_dq_id_seq', 5, false);
SELECT setval('pipelines_pipeline_id_seq', 2, false);
SELECT setval('pipeline_sources_pipeline_src_id_seq', 2, false);
SELECT setval('pipeline_targets_pipeline_tgt_id_seq', 2, false);
