INSERT INTO codes_hdr (id, description, type_cd) VALUES (1, 'User Role', 'role_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1, 1, 'ops-user', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2, 1, 'admin-user', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (3, 1, 'designer-user', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (2, 'Cloud Platform', 'platform_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (101, 2, 'Amazon Web Services', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (102, 2, 'Google Cloud Platform', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (103, 2, 'Microsoft Azure', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (104, 2, 'Bighammer (14 day trial)', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (3, 'Cloud platform Access Type', 'platform_access_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (201, 3, 'Access Key', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (202, 3, 'Role ARN', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (4, 'Project Environment', 'environment_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (301, 4, 'Development', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (302, 4, 'Testing', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (303, 4, 'UAT', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (304, 4, 'Staging', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (305, 4, 'Production', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (306, 4, 'Disaster Recovery', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (5, 'Data Zone', 'zone_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (401, 5, 'Bronze Zone', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (402, 5, 'Silver Zone', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (403, 5, 'Gold Zone', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (404, 5, 'Log Zone', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (405, 5, 'Quarantine Zone', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (6, 'Zone Type (Standard / Archive)', 'zone_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (501, 6, 'Standard Zone', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (502, 6, 'Archive Zone', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (7, 'Project Status', 'project_status_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (601, 7, 'Enable', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (602, 7, 'Disable', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (603, 7, 'Draft', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (8, 'Data Source Status', 'data_lake_status_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (701, 8, 'Active', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (702, 8, 'Inactive', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (703, 8, 'Draft', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (9, 'Customer Status', 'customer_status_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (801, 9, 'Active', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (802, 9, 'Inactive', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (803, 9, 'Draft', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (10, 'Target Delivery Platform', 'delivery_platform_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (901, 10, 'Snowflake-Warehouse', 11);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (902, 10, 'AWS - Redshift (WareHouse)', 12);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (903, 10, 'AWS - S3 (Object Storage)', 12);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (904, 10, 'GCP - Cloud  (Object Storage)', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (905, 10, 'GCP - BigQuery (Warehouse)', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (906, 10, 'Databricks-Delta Lake', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (11, 'Connection Parameters', 'connection_param_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1001, 11, 'URL', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1002, 11, 'User Name', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1003, 11, 'Password', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1004, 11, 'Warehouse', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (12, 'Platform Access Parameter', 'access_param_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1101, 12, 'Access_Key', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1102, 12, 'Secret_Access_Key', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (13, 'Data Types', 'data_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1201, 13, 'Integer', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1202, 13, 'String', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1203, 13, 'Date', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1204, 13, 'Timestamp', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1205, 13, 'Boolean', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1206, 13, 'Json', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1207, 13, 'Array', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1208, 13, 'Binary', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1209, 13, 'Decimal', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1210, 13, 'Double', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1211, 13, 'Float', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1212, 13, 'Long', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1213, 13, 'Short', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1214, 13, 'Byte', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1215, 13, 'map', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1216, 13, 'Struct', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (14, 'Join Types', 'join_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1301, 14, 'Left Outer Join', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1302, 14, 'Right Outer Join', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1303, 14, 'Inner Join', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1304, 14, 'Full Outer Join', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (15, 'Pipeline Type Codes', 'pipeline_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1401, 15, 'Onboarding Pipeline', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1402, 15, 'Code Pipeline', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1403, 15, 'Designer Pipeline', 0);


INSERT INTO codes_hdr (id, description, type_cd) VALUES (16, 'Layout Formats', 'layout_fmt_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1501, 16, 'Delimited', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1502, 16, 'Fixed Width', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1503, 16, 'Json', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1504, 16, 'Parquet', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1505, 16, 'XML', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1506, 16, 'XLSX', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1507, 16, 'CSV', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (17, 'Delimiter Types', 'delimiter_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1601, 17, 'Comma', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1602, 17, 'Tab', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1603, 17, 'Pipe', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1604, 17, 'Tilde', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1605, 17, 'Colon', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1606, 17, 'Semi Colon', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1607, 17, 'Space', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1608, 17, 'Double Quotes', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1609, 17, 'Single Quotes', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1610, 17, 'Custom Delimiter', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (18, 'Encoding Types', 'encoding_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1701, 18, 'UTF-8', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1702, 18, 'UTF-16', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1703, 18, 'ISO-8859-1', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1704, 18, 'Windows-1252', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1705, 18, 'US-ASCII', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1706, 18, 'UTF-8-SIG', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1707, 18, 'LATIN-1', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1708, 18, 'UNKNOWN', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (19, 'Quote Character Types', 'quote_char_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1801, 19, 'Double Quotes', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1802, 19, 'Single Quotes', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1803, 19, 'Backward Slash', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1804, 19, 'Forward Slash', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1805, 19, 'None', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (20, 'Escape Character Types', 'escape_char_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1901, 20, 'Backward Slash', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1902, 20, 'Forward Slash', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1903, 20, 'Single Quotes', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1904, 20, 'Double Quotes', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (1905, 20, 'None', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (21, 'Layout Type', 'lyt_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2001, 21, 'Master', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2002, 21, 'Child', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (22, 'Is Admin', 'is_admin_status_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2101, 22, 'Yes', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2102, 22, 'No', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2103, 7, 'Disable', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (23, 'Data Zone Type', 'data_zone_type_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2104, 23, 'Silver Zone', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2105, 23, 'Gold Zone', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (24, 'Delivery Option', 'delivery_option_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2106, 24, 'Full ', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2107, 24, 'Incremental', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (25, 'File Format', 'file_format_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2108, 25, 'CSV ', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2109, 25, 'Parquet', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2110, 25, 'JSON', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (26, 'Delimiter', 'delimiter_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2111, 26, 'Comma ', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2112, 26, 'Pipe', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2113, 26, 'Tilda', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (27, 'Compression', 'compression');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2114, 27, 'Bz2 ', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2115, 27, 'Zip', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2116, 27, 'Gz', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2117, 27, 'Snappy', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (28, 'Schedule Option', 'schedule_option');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2118, 28, 'Real Time ', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2119, 28, 'Schedule', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (29, 'Alert Status', 'alert_status');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2120, 29, 'Open', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2121, 29, 'In Progress', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (2122, 29, 'Closed', 0);

INSERT INTO codes_hdr (id, description, type_cd) VALUES (30, 'Github Providers', 'github_cd');
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (4100, 30, 'Github', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (4101, 30, 'Github Enterprise', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (4102, 30, 'Azure DevOps', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (4103, 30, 'Bitbucket', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (4104, 30, 'Gitlab', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (4105, 30, 'Git Lab Enterprise', 0);
INSERT INTO codes_dtl (id, codes_hdr_id, dtl_desc, dtl_id_filter) VALUES (4106, 30, 'Other', 0);


--platform_region table insert query
-------------------------------------

INSERT INTO platform_region (id, description, region_identifier, platform_cd)
VALUES 
(1, 'US East (Ohio | us-east-2)', 'us-east-2', 101),
(2, 'US East (N. Virginia | us-east-1)', 'us-east-1', 101),
(3, 'US West (N. California | us-west-1)', 'us-west-1', 101),
(4, 'US West (Oregon | us-west-2)', 'us-west-2', 101),
(5, 'Africa (Cape Town | af-south-1)', 'af-south-1', 101),
(6, 'Asia Pacific (Hong Kong | ap-east-1)', 'ap-east-1', 101),
(7, 'Asia Pacific (Hyderabad | ap-south-2)', 'ap-south-2', 101),
(8, 'Asia Pacific (Jakarta | ap-southeast-3)', 'ap-southeast-3', 101),
(9, 'Asia Pacific (Melbourne | ap-southeast-4)', 'ap-southeast-4', 101),
(10, 'Asia Pacific (Mumbai | ap-south-1)', 'ap-south-1', 101),
(11, 'Asia Pacific (Osaka | ap-northeast-3)', 'ap-northeast-3', 101),
(12, 'Asia Pacific (Seoul | ap-northeast-2)', 'ap-northeast-2', 101),
(13, 'Asia Pacific (Singapore | ap-southeast-1)', 'ap-southeast-1', 101),
(14, 'Asia Pacific (Sydney | ap-southeast-2)', 'ap-southeast-2', 101),
(15, 'Asia Pacific (Tokyo | ap-northeast-1)', 'ap-northeast-1', 101),
(16, 'Canada (Central | ca-central-1)', 'ca-central-1', 101),
(17, 'Canada West (Calgary | ca-west-1)', 'ca-west-1', 101),
(18, 'Europe (Frankfurt | eu-central-1)', 'eu-central-1', 101),
(19, 'Europe (Ireland | eu-west-1)', 'eu-west-1', 101),
(20, 'Europe (London | eu-west-2)', 'eu-west-2', 101),
(21, 'Europe (Milan | eu-south-1)', 'eu-south-1', 101),
(22, 'Europe (Paris | eu-west-3)', 'eu-west-3', 101),
(23, 'Europe (Spain | eu-south-2)', 'eu-south-2', 101),
(24, 'Europe (Stockholm | eu-north-1)', 'eu-north-1', 101),
(25, 'Europe (Zurich | eu-central-2)', 'eu-central-2', 101),
(26, 'Israel (Tel Aviv | il-central-1)', 'il-central-1', 101),
(27, 'Middle East (Bahrain | me-south-1)', 'me-south-1', 101),
(28, 'Middle East (UAE | me-central-1)', 'me-central-1', 101),
(29, 'South America (São Paulo | sa-east-1)', 'sa-east-1', 101),
(30, 'AWS GovCloud (US-East | us-gov-east-1)', 'us-gov-east-1', 101),
(31, 'AWS GovCloud (US-West | us-gov-west-1)', 'us-gov-west-1', 101);
