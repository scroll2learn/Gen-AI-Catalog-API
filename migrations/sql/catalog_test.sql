

INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 21, 'People', 'Person statistics', '2024-07-02 14:50:00', '0%', 701, 1, 'user_profile');

INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (21, 'User Details', 'Census Bureau', 999, 999, 21, 'demographics_agency');

INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (221, 'User Details Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 21, 'userDetail', 2001, true, False);
 
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"user": "User Details"}', 281, 'id', 'Availability of User Details', 10, False, 0, 10, 1203, 221, 'userId', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"user": "User Details"}', 282, 'name', 'Availability of User Details', 10, False, 0, 10, 1203, 221, 'user name', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"user": "User Details"}', 283, 'age', 'Availability of User Details', 10, False, 0, 10, 1203, 221, 'user age', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"user": "User Details"}', 284, 'city', 'Availability of User Details', 10, False, 0, 10, 1203, 221, 'user city', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"user": "User Details"}', 285, 'address', 'Availability of User Details', 10, False, 0, 10, 1203, 221, 'user address', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"user": "User Details"}', 286, 'state', 'Availability of User Details', 10, False, 0, 10, 1203, 221, 'user state', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"user": "User Details"}', 287, 'zip', 'Availability of User Details', 10, False, 0, 10, 1203, 221, 'zipcode', False);

 