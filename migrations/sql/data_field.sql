

INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (201, 'Electric Vechicle Population Data Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\.csv$', True, 1, 'datalayout', 2001, true, False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"vehicles": "Vehicle", "counts": "Count"}', 102, 'Vehicle Count', 'Electric Vehicle Data', 2, False, 0, 10, 1202, 201, 'vehiclecount', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"distance": "Distance"}', 103, 'Total Distance Covered', 'Electric Vehicle Data', 3, False, 0, 0, 1201, 201, 'distancecovered', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"power": "power", "energy": "energy", "consumption": "consumption"}', 104, 'Average Energy Consumption', 'Electric Vehicle Data', 4, False, 0, 10, 1202, 201, 'energyconsumption', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"station": "Station", "charger": "charger"}', 105, 'Charging Stations Count', 'Electric Vehicle Data', 5, False, 0, 0, 1204, 201, 'chargingstations', False);


INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 2, 'Air Quality', 'This is Air Quality', '2024-06-11 07:06:58', '0%', 701, 1, 'air_quality');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 3, 'Public Transport', 'Bus and train schedules', '2024-06-15 12:00:00', '0%', 701, 1, 'public_transport');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 4, 'Climate Data', 'Climate metrics and analysis', '2024-06-16 13:45:20', '0%', 701, 1, 'climate_data');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 5, 'Hospital Facilities', 'Data on hospital facilities', '2024-06-17 09:30:00', '0%', 701, 1, 'hospital_facilities');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 6, 'School Enrollment', 'Student enrollment statistics', '2024-06-18 08:15:45', '0%', 701, 1, 'school_enrollment');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 7, 'Unemployment Rate', 'Monthly unemployment rates', '2024-06-19 11:20:00', '0%', 701, 1, 'unemployment_rate');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 8, 'Crime Statistics', 'Monthly crime reports', '2024-06-20 14:10:25', '0%', 701, 1, 'crime_statistics');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 9, 'Water Quality', 'Analysis of water quality', '2024-06-21 16:35:15', '0%', 701, 1, 'water_quality');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 10, 'Road Conditions', 'Data on road maintenance', '2024-06-22 13:25:00', '0%', 701, 1, 'road_conditions');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 11, 'Affordable Housing', 'Data on housing availability', '2024-06-23 10:05:45', '0%', 701, 1, 'affordable_housing');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 12, 'Workforce Statistics', 'Employment and workforce trends', '2024-06-24 09:40:30', '0%', 701, 1, 'workforce_statistics');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 13, 'Crop Yield', 'Annual crop yield statistics', '2024-06-25 11:50:00', '0%', 701, 1, 'crop_yield');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 14, 'Tax Revenue', 'Government tax revenue data', '2024-06-26 13:30:00', '0%', 701, 1, 'tax_revenue');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 15, 'Energy Consumption', 'Energy usage statistics', '2024-06-27 09:45:00', '0%', 701, 1, 'energy_consumption');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 16, 'Traffic Patterns', 'Traffic flow and congestion data', '2024-06-28 14:15:00', '0%', 701, 1, 'traffic_patterns');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 17, 'Disease Outbreaks', 'Data on infectious diseases', '2024-06-29 10:25:00', '0%', 701, 1, 'disease_outbreaks');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 18, 'Literacy Rates', 'Literacy rate statistics by region', '2024-06-30 12:35:00', '0%', 701, 1, 'literacy_rates');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 19, 'Internet Usage', 'Data on internet access and usage', '2024-07-01 11:00:00', '0%', 701, 1, 'internet_usage');
INSERT INTO data_source (data_src_tags, data_src_id, data_src_name, data_src_desc, data_src_last_updated, data_src_quality, data_src_status_cd, lake_zone_id, data_src_key) VALUES ('{"key":"value"}', 20, 'Population Growth', 'Annual population growth statistics', '2024-07-02 14:50:00', '0%', 701, 1, 'population_growth');

INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (2, 'City Corporation', 'city User', 999, 999, 2, 'citycoporation');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (3, 'Agency', 'Transit Authority', 999, 999, 3, 'agency');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (4, 'Region', 'Global', 999, 999, 4, 'region');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (5, 'Department', 'Health Ministry', 999, 999, 5, 'department');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (6, 'School Board', 'Local Board', 999, 999, 6, 'school_board');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (7, 'Economic Zone', 'Urban', 999, 999, 7, 'economic_zone');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (8, 'Police Division', 'Metro Police', 999, 999, 8, 'police_division');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (9, 'Water Authority', 'State Water Dept', 999, 999, 9, 'water_authority');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (10, 'Transport Ministry', 'State Transport', 999, 999, 10, 'transport_ministry');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (11, 'Housing Board', 'Affordable Housing Board', 999, 999, 11, 'housing_board');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (12, 'Labor Dept', 'National Labor Dept', 999, 999, 12, 'labor_dept');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (13, 'Agriculture Dept', 'National Agriculture Agency', 999, 999, 13, 'agriculture_dept');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (14, 'Finance Dept', 'Revenue Office', 999, 999, 14, 'finance_dept');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (15, 'Energy Board', 'Energy Analytics Dept', 999, 999, 15, 'energy_board');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (17, 'Health Agency', 'Disease Control Unit', 999, 999, 17, 'health_agency');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (18, 'Education Dept', 'State Literacy Board', 999, 999, 18, 'education_dept');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (19, 'Tech Ministry', 'Internet Access Division', 999, 999, 19, 'tech_ministry');
INSERT INTO data_source_metadata (data_src_mtd_id, data_src_mtd_name, data_src_mtd_value, data_src_mtd_datatype_cd, data_src_mtd_type_cd, data_src_id, data_src_mtd_key) VALUES (20, 'Demographics Agency', 'Census Bureau', 999, 999, 20, 'demographics_agency');

INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (202, 'Air Quality Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 2, 'corporationschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (203, 'Public Transport Data Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 3, 'demoschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (204, 'Climate Data Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 4, 'climateschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (205, 'Hospital Facilities Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 5, 'hospitalschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (206, 'School Enrollment Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 6, 'schoolschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (207, 'Unemployment Rate Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 7, 'unemploymentschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (208, 'Crime Statistics Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 8, 'crimeschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (209, 'Water Quality Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 9, 'waterschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (210, 'Road Conditions Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 10, 'roadschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (211, 'Affordable Housing Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 11, 'housingschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (212, 'Workforce Statistics Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 12, 'workforceschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (213, 'Crop Yield Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 13, 'cropschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (214, 'Tax Revenue Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 14, 'taxschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (215, 'Energy Consumption Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 15, 'energyschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (216, 'Traffic Patterns Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 16, 'trafficschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (217, 'Disease Outbreaks Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 17, 'diseaseschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (218, 'Literacy Rates Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 18, 'literacyschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (219, 'Internet Usage Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 19, 'internetschema', 2001, true, False);
INSERT INTO data_source_layout (data_src_lyt_id, data_src_lyt_name, data_src_lyt_fmt_cd, data_src_lyt_delimiter_cd, data_src_lyt_cust_delimiter, data_src_lyt_header, data_src_lyt_encoding_cd, data_src_lyt_quote_chars_cd, data_src_lyt_escape_chars_cd, data_src_lyt_regex, data_src_lyt_pk, data_src_id, data_src_lyt_key, data_src_lyt_type_cd, data_src_lyt_is_mandatory, is_deleted) VALUES (220, 'Population Growth Schema', 1501, 1601, null, True, 1701, 1801, 1905, '.*\\.csv$', True, 20, 'populationschema', 2001, true, False);


INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"air": "air", "index": "index"}', 106, 'Air Quality Index', 'Air Quality Index Data', 2, False, 0, 10, 1202, 202, 'airqualityindex', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"pm": "PM2.5"}', 107, 'Particulate Matter 2.5', 'Air Quality Index Data', 3, False, 0, 0, 1201, 202, 'particulatematter', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"gas": "NO2", "level":"non-toxic"}', 108, 'NO2 Level', 'Air Quality Index Data', 3, False, 0, 0, 1201, 202, 'nolevel', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"gas": "temp", "c":"celusis", "f":"Fahrenheit"}', 109, 'Temperature', 'Air Quality Index Data', 3, False, 0, 0, 1201, 202, 'temperature', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"gas": "air", "time":"time"}', 110, 'Measurement Time', 'Air Quality Index Data', 3, False, 0, 0, 1201, 202, 'measurementtime:', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"gas": "station"}', 11, 'Station ID', 'Air Quality Index Data', 3, False, 0, 0, 1201, 202, 'stationid:', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"route": "Route Number"}', 111, 'Route Number', 'Public transport route numbers', 1, False, 0, 10, 1203, 203, 'routenumber', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"schedule": "Schedule"}', 112, 'Schedule Time', 'Bus and train schedules', 2, False, 0, 15, 1204, 203, 'scheduletime', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"stop": "Stop"}', 113, 'Stop Name', 'Name of the stop/station', 3, False, 0, 25, 1201, 203, 'stopname', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"passenger": "Passenger Count"}', 114, 'Passenger Count', 'Number of passengers per route', 4, False, 0, 5, 1202, 203, 'passengercount', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"driver": "Driver Info"}', 115, 'Driver Name', 'Information about the driver', 5, False, 0, 30, 1201, 203, 'driverinfo', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"temperature": "Temperature"}', 116, 'Average Temperature', 'Daily average temperature recorded', 1, False, 0, 10, 1203, 204, 'avgtemperature', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"precipitation": "Precipitation"}', 117, 'Total Precipitation', 'Daily total precipitation levels', 2, False, 0, 10, 1202, 204, 'totalprecipitation', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"wind_speed": "Wind Speed"}', 118, 'Average Wind Speed', 'Daily average wind speed', 3, False, 0, 10, 1203, 204, 'avgwindspeed', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"humidity": "Humidity"}', 119, 'Average Humidity', 'Daily average humidity percentage', 4, False, 0, 5, 1202, 204, 'avghumidity', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"solar_radiation": "Solar Radiation"}', 120, 'Solar Radiation Index', 'Daily average solar radiation index', 5, False, 0, 10, 1202, 204, 'solarradiation', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"pressure": "Air Pressure"}', 121, 'Atmospheric Pressure', 'Average atmospheric pressure', 6, False, 0, 10, 1204, 204, 'avgpressure', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"cloud_cover": "Cloud Cover"}', 122, 'Cloud Cover Percentage', 'Percentage of cloud cover throughout the day', 7, False, 0, 5, 1202, 204, 'cloudcover', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"visibility": "Visibility"}', 123, 'Average Visibility', 'Daily average visibility in kilometers', 8, False, 0, 10, 1204, 204, 'avgvisibility', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"uv_index": "UV Index"}', 124, 'Maximum UV Index', 'Maximum UV index recorded during the day', 9, False, 0, 5, 1202, 204, 'maxuvindex', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"dew_point": "Dew Point"}', 125, 'Average Dew Point', 'Daily average dew point temperature', 10, False, 0, 10, 1204, 204, 'avgdewpoint', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"hospital_name": "Hospital Name"}', 126, 'Hospital Name', 'Name of the hospital', 1, False, 0, 50, 1203, 205, 'hospitalname', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"location": "Location"}', 127, 'Location', 'Location of the hospital', 2, False, 0, 50, 1203, 205, 'hospitalocation', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"beds": "Bed Count"}', 128, 'Bed Count', 'Number of beds available', 3, False, 0, 10, 1202, 205, 'bedcount', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"icu": "ICU Availability"}', 129, 'ICU Availability', 'Number of ICU beds available', 4, False, 0, 10, 1202, 205, 'icuavailability', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"ventilators": "Ventilators Count"}', 130, 'Ventilators Count', 'Number of ventilators available', 5, False, 0, 10, 1202, 205, 'ventilatorscount', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"staff": "Staff Count"}', 131, 'Staff Count', 'Total medical and support staff', 6, False, 0, 10, 1202, 205, 'staffcount', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"emergency": "Emergency Services"}', 132, 'Emergency Services Available', 'Availability of emergency services', 7, False, 0, 10, 1203, 205, 'emergencyservices', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"specialty": "Specialty Services"}', 133, 'Specialty Services Offered', 'List of specialty medical services', 8, False, 0, 100, 1203, 205, 'specialtyservices', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"operating_rooms": "Operating Rooms"}', 134, 'Operating Rooms Count', 'Number of operating rooms', 9, False, 0, 10, 1202, 205, 'operatingrooms', False);
INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) VALUES ('{"laboratory": "Laboratory Services"}', 135, 'Laboratory Services Available', 'Availability of laboratory services', 10, False, 0, 10, 1203, 205, 'laboratoryservices', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"school": "School Name"}', 136, 'School Name', 'Name of the school', 1, False, 0, 50, 1203, 206, 'schoolname', False),
('{"enrollment": "Enrollment Count"}', 137, 'Enrollment Count', 'Total number of enrolled students', 2, False, 0, 10, 1202, 206, 'enrollmentcount', False),
('{"grade": "Grade", "level": "Level"}', 138, 'Grade Level', 'Grade or level of the students', 3, False, 0, 20, 1203, 206, 'gradelevel', False),
('{"gender": "Gender", "ratio": "Ratio"}', 139, 'Gender Ratio', 'Male-to-female ratio in the school', 4, False, 0, 10, 1202, 206, 'genderratio', False),
('{"teacher": "Teacher Count"}', 140, 'Teacher Count', 'Number of teachers in the school', 5, False, 0, 10, 1202, 206, 'teachercount', False),
('{"classroom": "Classroom Count", "facilities": "Facilities"}', 141, 'Classroom Count', 'Number of classrooms available', 6, False, 0, 10, 1202, 206, 'classroomcount', False),
('{"program": "Programs", "extracurricular": "Extracurricular"}', 142, 'Programs Offered', 'Details of programs and extracurricular activities', 7, False, 0, 100, 1203, 206, 'programsoffered', False),
('{"student": "Student-Teacher Ratio"}', 143, 'Student-Teacher Ratio', 'Ratio of students to teachers', 8, False, 0, 10, 1202, 206, 'studentteacherratio', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"region": "Region"}', 144, 'Region Name', 'Name of the region or area', 1, False, 0, 50, 1203, 207, 'regionname', False),
('{"month": "Month", "year": "Year"}', 145, 'Reporting Month', 'Month and year of the report', 2, False, 0, 20, 1203, 207, 'reportingmonth', False),
('{"rate": "Unemployment Rate"}', 146, 'Unemployment Rate', 'Percentage of unemployed individuals', 3, False, 0, 10, 1202, 207, 'unemploymentrate', False),
('{"age": "Age Group"}', 147, 'Age Group', 'Age group of individuals reported', 4, False, 0, 30, 1203, 207, 'agegroup', False),
('{"gender": "Gender", "ratio": "Ratio"}', 148, 'Gender Ratio', 'Male-to-female unemployment ratio', 5, False, 0, 10, 1202, 207, 'genderratio', False),
('{"industry": "Industry", "sector": "Sector"}', 149, 'Industry Sector', 'Sector or industry affected', 6, False, 0, 50, 1203, 207, 'industrysector', False),
('{"duration": "Duration"}', 150, 'Unemployment Duration', 'Average duration of unemployment in months', 7, False, 0, 10, 1202, 207, 'unemploymentduration', False),
('{"education": "Education Level"}', 151, 'Education Level', 'Education level of unemployed individuals', 8, False, 0, 50, 1203, 207, 'educationlevel', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"region": "Region"}', 152, 'Region Name', 'Name of the region or area', 1, False, 0, 50, 1203, 208, 'regionname', False),
('{"month": "Month", "year": "Year"}', 153, 'Reporting Month', 'Month and year of the crime report', 2, False, 0, 20, 1203, 208, 'reportingmonth', False),
('{"crime": "Crime Type"}', 154, 'Crime Type', 'Type of crime reported', 3, False, 0, 30, 1203, 208, 'crimetype', False),
('{"count": "Crime Count"}', 155, 'Crime Count', 'Number of crimes reported', 4, False, 0, 10, 1202, 208, 'crimecount', False),
('{"age": "Age Group"}', 156, 'Age Group', 'Age group of individuals involved', 5, False, 0, 30, 1203, 208, 'agegroup', False),
('{"gender": "Gender", "ratio": "Ratio"}', 157, 'Gender Ratio', 'Male-to-female crime ratio', 6, False, 0, 10, 1202, 208, 'genderratio', False),
('{"severity": "Severity", "classification": "Classification"}', 158, 'Crime Severity', 'Severity or classification of the crime', 7, False, 0, 30, 1203, 208, 'crimeseverity', False),
('{"location": "Location", "coordinates": "Coordinates"}', 159, 'Crime Location', 'Location or coordinates of the crime', 8, False, 0, 50, 1203, 208, 'crimelocation', False),
('{"arrests": "Arrests"}', 160, 'Arrests Made', 'Number of arrests made in connection to the crimes', 9, False, 0, 10, 1202, 208, 'arrestsmade', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"location": "Location"}', 161, 'Sampling Location', 'Location where water sample was collected', 1, False, 0, 50, 1203, 209, 'samplinglocation', False),
('{"date": "Sampling Date", "time": "Sampling Time"}', 162, 'Sampling Date and Time', 'Date and time of sample collection', 2, False, 0, 25, 1203, 209, 'samplingdatetime', False),
('{"ph": "pH"}', 163, 'pH Level', 'pH level of the water sample', 3, False, 0, 10, 1202, 209, 'phlevel', False),
('{"turbidity": "Turbidity"}', 164, 'Turbidity Level', 'Turbidity measurement of the water', 4, False, 0, 10, 1202, 209, 'turbiditylevel', False),
('{"contaminants": "Contaminants", "chemicals": "Chemicals"}', 165, 'Contaminant Levels', 'Levels of harmful contaminants or chemicals', 5, False, 0, 50, 1203, 209, 'contaminantlevels', False),
('{"hardness": "Hardness"}', 166, 'Water Hardness', 'Measurement of water hardness', 6, False, 0, 10, 1202, 209, 'waterhardness', False),
('{"oxygen": "Dissolved Oxygen", "levels": "Levels"}', 167, 'Dissolved Oxygen Level', 'Level of dissolved oxygen in the water', 7, False, 0, 10, 1202, 209, 'dissolvedoxygen', False),
('{"temperature": "Temperature"}', 168, 'Water Temperature', 'Temperature of the water sample', 8, False, 0, 10, 1202, 209, 'watertemperature', False),
('{"conductivity": "Conductivity"}', 169, 'Electrical Conductivity', 'Electrical conductivity of the water', 9, False, 0, 10, 1202, 209, 'electricalconductivity', False),
('{"bacteria": "Bacteria"}', 170, 'Bacterial Contamination', 'Presence of bacterial contamination in water', 10, False, 0, 10, 1203, 209, 'bacterialcontamination', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"location": "Location"}', 171, 'Road Location', 'Specific road location or section', 1, False, 0, 50, 1203, 210, 'roadlocation', False),
('{"date": "Inspection Date"}', 172, 'Inspection Date', 'Date of road inspection or report', 2, False, 0, 25, 1203, 210, 'inspectiondate', False),
('{"condition": "Condition", "rating": "Rating"}', 173, 'Condition Rating', 'Rating of road condition', 3, False, 0, 10, 1202, 210, 'conditionrating', False),
('{"potholes": "Potholes"}', 174, 'Number of Potholes', 'Count of potholes on the road', 4, False, 0, 10, 1202, 210, 'numberofpotholes', False),
('{"traffic": "Traffic", "volume": "Volume"}', 175, 'Traffic Volume', 'Average traffic volume on the road', 5, False, 0, 15, 1202, 210, 'trafficvolume', False),
('{"accidents": "Accidents"}', 176, 'Accident Reports', 'Number of accidents reported', 6, False, 0, 10, 1202, 210, 'accidentreports', False),
('{"material": "Material", "type": "Type"}', 177, 'Road Material Type', 'Type of material used for the road', 7, False, 0, 30, 1203, 210, 'roadmaterialtype', False),
('{"repairs": "Repairs", "status": "Status"}', 178, 'Repair Status', 'Current status of road repairs', 8, False, 0, 20, 1203, 210, 'repairstatus', False),
('{"width": "Width"}', 179, 'Road Width', 'Width of the road in meters', 9, False, 0, 10, 1202, 210, 'roadwidth', False),
('{"length": "Length"}', 180, 'Road Length', 'Length of the road in kilometers', 10, False, 0, 10, 1202, 210, 'roadlength', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"location": "Location"}', 181, 'Housing Location', 'Geographic location of affordable housing units', 1, False, 0, 50, 1203, 211, 'housinglocation', False),
('{"unit_type": "Unit Type", "category": "Category"}', 182, 'Unit Type and Category', 'Type of housing unit (e.g., apartment, house)', 2, False, 0, 30, 1203, 211, 'unittypecategory', False),
('{"price": "Price"}', 183, 'Price of Unit', 'Price of the housing unit', 3, False, 0, 10, 1202, 211, 'priceofunit', False),
('{"size": "Size", "sq_ft": "Square Feet"}', 184, 'Unit Size', 'Size of the housing unit in square feet', 4, False, 0, 10, 1202, 211, 'unitsize', False),
('{"beds": "Bedrooms"}', 185, 'Number of Bedrooms', 'Number of bedrooms in the unit', 5, False, 0, 10, 1202, 211, 'numberofbedrooms', False),
('{"baths": "Bathrooms"}', 186, 'Number of Bathrooms', 'Number of bathrooms in the unit', 6, False, 0, 10, 1202, 211, 'numberofbathrooms', False),
('{"availability": "Availability", "status": "Status"}', 187, 'Availability Status', 'Availability status of the housing unit (e.g., available, under construction)', 7, False, 0, 30, 1203, 211, 'availablestatus', False),
('{"income": "Income", "requirements": "Income Requirements"}', 188, 'Income Requirements', 'Income thresholds for qualification', 8, False, 0, 30, 1203, 211, 'incomerequirements', False),
('{"age": "Age", "restriction": "Age Restriction"}', 189, 'Age Restriction', 'Age restrictions for housing eligibility', 9, False, 0, 20, 1203, 211, 'agerestriction', False),
('{"region": "Region"}', 190, 'Region', 'Region or area for the housing project', 10, False, 0, 50, 1203, 211, 'region', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"location": "Location"}', 191, 'Workforce Location', 'Geographic location of the workforce data', 1, False, 0, 50, 1203, 212, 'workforcelocation', False),
('{"sector": "Sector"}', 192, 'Industry Sector', 'Industry sector of the workforce (e.g., manufacturing, IT)', 2, False, 0, 30, 1203, 212, 'industrysector', False),
('{"employment": "Employment", "status": "Status"}', 193, 'Employment Status', 'Employment status of the workforce (employed, unemployed, etc.)', 3, False, 0, 20, 1203, 212, 'employmentstatus', False),
('{"education": "Education"}', 194, 'Education Level', 'Education level of the workforce (e.g., high school, college, etc.)', 4, False, 0, 30, 1203, 212, 'educationlevel', False),
('{"age": "Age", "group": "Age Group"}', 195, 'Age Group', 'Age group classification of the workforce', 5, False, 0, 20, 1203, 212, 'agegroup', False),
('{"gender": "Gender"}', 196, 'Gender', 'Gender classification of the workforce', 6, False, 0, 10, 1202, 212, 'gender', False),
('{"wage": "Wage"}', 197, 'Wage Level', 'Average wage level for the workforce in the sector', 7, False, 0, 10, 1202, 212, 'wagelevel', False),
('{"hours": "Hours"}', 198, 'Average Weekly Hours', 'Average number of weekly working hours', 8, False, 0, 10, 1202, 212, 'averageweeklyhours', False),
('{"experience": "Experience"}', 199, 'Experience Level', 'Years of experience of the workforce', 9, False, 0, 10, 1202, 212, 'experiencelevel', False),
('{"unemployment": "Unemployment"}', 200, 'Unemployment Rate', 'Unemployment rate in the region or sector', 10, False, 0, 10, 1202, 212, 'unemploymentrate', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"location": "Location"}', 201, 'Crop Location', 'Geographic location of crop yield data', 1, False, 0, 50, 1203, 213, 'croplocation', False),
('{"crop_type": "Crop Type"}', 202, 'Crop Type', 'Type of crop being harvested', 2, False, 0, 30, 1203, 213, 'croptype', False),
('{"yield": "Yield"}', 203, 'Annual Yield', 'Amount of crop yield per year in tons or kilograms', 3, False, 0, 10, 1202, 213, 'annualyield', False),
('{"area": "Area"}', 204, 'Area Harvested', 'Total area harvested for the crop (in hectares or acres)', 4, False, 0, 10, 1202, 213, 'areaharvested', False),
('{"production": "Production"}', 205, 'Production Volume', 'Volume of crop production in kilograms or tons', 5, False, 0, 10, 1202, 213, 'productionvolume', False),
('{"month": "Month"}', 206, 'Month of Harvest', 'Month when the crop was harvested', 6, False, 0, 20, 1203, 213, 'monthofharvest', False),
('{"region": "Region"}', 207, 'Region', 'Region where the crop was produced', 7, False, 0, 50, 1203, 213, 'region', False),
('{"weather": "Weather"}', 208, 'Weather Conditions', 'Weather conditions that affected crop yield', 8, False, 0, 30, 1203, 213, 'weatherconditions', False),
('{"irrigation": "Irrigation"}', 209, 'Irrigation Used', 'Type and amount of irrigation used in crop cultivation', 9, False, 0, 30, 1203, 213, 'irrigationused', False),
('{"pesticides": "Pesticides"}', 210, 'Pesticide Usage', 'Amount of pesticides used during crop production', 10, False, 0, 10, 1202, 213, 'pesticideusage', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"location": "Location"}', 211, 'Tax Location', 'Geographic location of the tax revenue data', 1, False, 0, 50, 1203, 214, 'taxlocation', False),
('{"tax_type": "Tax Type"}', 212, 'Tax Type', 'Type of tax (e.g., income tax, sales tax, etc.)', 2, False, 0, 30, 1203, 214, 'taxtype', False),
('{"revenue": "Revenue"}', 213, 'Tax Revenue Amount', 'Amount of tax revenue collected', 3, False, 0, 10, 1202, 214, 'taxrevenueamount', False),
('{"month": "Month"}', 214, 'Month of Collection', 'Month when the tax revenue was collected', 4, False, 0, 20, 1203, 214, 'monthofcollection', False),
('{"year": "Year"}', 215, 'Year of Collection', 'Year when the tax revenue was collected', 5, False, 0, 10, 1202, 214, 'yearofcollection', False),
('{"source": "Source"}', 216, 'Tax Revenue Source', 'Source of the tax revenue (e.g., individual, corporate, etc.)', 6, False, 0, 30, 1203, 214, 'taxrevenuesource', False),
('{"amount": "Amount"}', 217, 'Amount Collected', 'Total amount collected from the tax source', 7, False, 0, 10, 1202, 214, 'amountcollected', False),
('{"region": "Region"}', 218, 'Region', 'Region where the tax revenue was collected', 8, False, 0, 50, 1203, 214, 'region', False),
('{"tax_rate": "Tax Rate"}', 219, 'Tax Rate', 'Tax rate applied for the revenue collected', 9, False, 0, 10, 1202, 214, 'taxrate', False),
('{"exemption": "Exemption"}', 220, 'Exemption Status', 'Exemption status for the tax (e.g., exempt, non-exempt)', 10, False, 0, 20, 1203, 214, 'exemptionstatus', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"location": "Location"}', 221, 'Energy Consumption Location', 'Geographic location of energy consumption data', 1, False, 0, 50, 1203, 215, 'energyconsumptionlocation', False),
('{"sector": "Sector"}', 222, 'Energy Consumption Sector', 'Sector or industry using the energy', 2, False, 0, 30, 1203, 215, 'energyconsumptionsector', False),
('{"energy_type": "Energy Type"}', 223, 'Type of Energy', 'Type of energy consumed (e.g., electricity, gas)', 3, False, 0, 20, 1203, 215, 'energytype', False),
('{"amount": "Amount"}', 224, 'Energy Consumption Amount', 'Amount of energy consumed (e.g., kWh, MWh)', 4, False, 0, 10, 1202, 215, 'energyconsumptionamount', False),
('{"unit": "Unit"}', 225, 'Energy Unit', 'Unit of measurement for energy (e.g., kWh, MWh)', 5, False, 0, 10, 1203, 215, 'energyunit', False),
('{"month": "Month"}', 226, 'Month of Consumption', 'Month when the energy was consumed', 6, False, 0, 20, 1203, 215, 'monthofconsumption', False),
('{"year": "Year"}', 227, 'Year of Consumption', 'Year when the energy was consumed', 7, False, 0, 10, 1202, 215, 'yearofconsumption', False),
('{"region": "Region"}', 228, 'Region', 'Region where the energy consumption data was recorded', 8, False, 0, 50, 1203, 215, 'region', False),
('{"source": "Energy Source"}', 229, 'Energy Source', 'Source of the energy consumed (e.g., renewable, fossil fuels)', 9, False, 0, 30, 1203, 215, 'energysource', False),
('{"efficiency": "Efficiency"}', 230, 'Energy Efficiency', 'Energy efficiency of the consumption process', 10, False, 0, 10, 1202, 215, 'energyefficiency', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"location": "Location"}', 231, 'Traffic Location', 'Geographic location of traffic data', 1, False, 0, 50, 1203, 216, 'trafficlocation', False),
('{"time_of_day": "Time of Day"}', 232, 'Time of Day', 'Time period during which traffic data was recorded', 2, False, 0, 30, 1203, 216, 'timeofday', False),
('{"traffic_flow": "Traffic Flow"}', 233, 'Traffic Flow', 'Traffic flow measured (e.g., number of vehicles per hour)', 3, False, 0, 10, 1202, 216, 'trafficflow', False),
('{"congestion_level": "Congestion Level"}', 234, 'Traffic Congestion Level', 'Level of congestion (e.g., low, moderate, high)', 4, False, 0, 20, 1203, 216, 'congestionlevel', False),
('{"vehicle_type": "Vehicle Type"}', 235, 'Vehicle Type', 'Types of vehicles involved in the traffic flow (e.g., cars, trucks)', 5, False, 0, 30, 1203, 216, 'vehicletype', False),
('{"accidents": "Accidents"}', 236, 'Traffic Accidents', 'Number of traffic accidents reported during the time period', 6, False, 0, 10, 1202, 216, 'trafficaccidents', False),
('{"road_condition": "Road Condition"}', 237, 'Road Condition', 'Condition of the road (e.g., wet, dry, under construction)', 7, False, 0, 20, 1203, 216, 'roadcondition', False),
('{"average_speed": "Average Speed"}', 238, 'Average Speed', 'Average speed of vehicles during the time period', 8, False, 0, 10, 1202, 216, 'averagespeed', False),
('{"direction": "Traffic Direction"}', 239, 'Traffic Direction', 'Direction of traffic flow (e.g., northbound, southbound)', 9, False, 0, 20, 1203, 216, 'trafficdirection', False),
('{"traffic_density": "Traffic Density"}', 240, 'Traffic Density', 'Density of vehicles (e.g., low, medium, high)', 10, False, 0, 20, 1203, 216, 'trafficdensity', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"disease": "Disease"}', 241, 'Disease Name', 'Name of the infectious disease', 1, False, 0, 50, 1203, 217, 'diseasename', False),
('{"location": "Location"}', 242, 'Outbreak Location', 'Geographic location of the outbreak', 2, False, 0, 50, 1203, 217, 'outbreaklocation', False),
('{"cases": "Cases"}', 243, 'Number of Cases', 'Number of reported cases of the disease', 3, False, 0, 10, 1202, 217, 'cases', False),
('{"deaths": "Deaths"}', 244, 'Number of Deaths', 'Number of deaths reported due to the disease', 4, False, 0, 10, 1202, 217, 'deaths', False),
('{"recovered": "Recovered"}', 245, 'Number of Recoveries', 'Number of recoveries from the disease', 5, False, 0, 10, 1202, 217, 'recoveries', False),
('{"symptoms": "Symptoms"}', 246, 'Common Symptoms', 'Common symptoms of the disease', 6, False, 0, 100, 1203, 217, 'symptoms', False),
('{"age_group": "Age Group"}', 247, 'Age Group Affected', 'Age group most affected by the disease', 7, False, 0, 20, 1203, 217, 'agegroup', False),
('{"gender": "Gender"}', 248, 'Gender Affected', 'Gender distribution of the cases', 8, False, 0, 10, 1203, 217, 'genderaffected', False),
('{"transmission": "Transmission Mode"}', 249, 'Mode of Transmission', 'How the disease is transmitted (e.g., airborne, contact)', 9, False, 0, 30, 1203, 217, 'transmissionmode', False),
('{"vaccine": "Vaccine Status"}', 250, 'Vaccine Availability', 'Status of vaccine availability for the disease', 10, False, 0, 30, 1203, 217, 'vaccinestatus', False);


INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"region": "Region"}', 251, 'Region', 'Geographic region where literacy rates are measured', 1, False, 0, 50, 1203, 218, 'region', False),
('{"total_population": "Total Population"}', 252, 'Total Population', 'Total population of the region', 2, False, 0, 10, 1202, 218, 'totalpopulation', False),
('{"literacy_rate": "Literacy Rate"}', 253, 'Literacy Rate', 'Percentage of the population that is literate', 3, False, 0, 10, 1202, 218, 'literacyrate', False),
('{"male_literacy": "Male Literacy Rate"}', 254, 'Male Literacy Rate', 'Literacy rate among male population', 4, False, 0, 10, 1202, 218, 'maleliteracy', False),
('{"female_literacy": "Female Literacy Rate"}', 255, 'Female Literacy Rate', 'Literacy rate among female population', 5, False, 0, 10, 1202, 218, 'femaleliteracy', False),
('{"age_group": "Age Group"}', 256, 'Age Group', 'Age group for which the literacy rate is measured', 6, False, 0, 30, 1203, 218, 'agegroup', False),
('{"literacy_def": "Literacy Definition"}', 257, 'Literacy Definition', 'Definition of literacy used in the measurement (e.g., reading, writing)', 7, False, 0, 100, 1203, 218, 'literacydef', False),
('{"education_level": "Education Level"}', 258, 'Education Level', 'Highest level of education achieved in the region', 8, False, 0, 30, 1203, 218, 'educationlevel', False),
('{"year": "Year"}', 259, 'Year', 'Year in which literacy rates were measured', 9, False, 0, 4, 1202, 218, 'year', False),
('{"data_source": "Data Source"}', 260, 'Data Source', 'Source of the literacy data (e.g., survey, census)', 10, False, 0, 50, 1203, 218, 'datasource', False);


INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"region": "Region"}', 261, 'Region', 'Geographic region where internet usage data is collected', 1, False, 0, 50, 1203, 219, 'region', False),
('{"internet_access": "Internet Access"}', 262, 'Internet Access Rate', 'Percentage of the population with internet access', 2, False, 0, 10, 1202, 219, 'internetaccessrate', False),
('{"age_group": "Age Group"}', 263, 'Age Group', 'Age group for which internet usage is measured', 3, False, 0, 30, 1203, 219, 'agegroup', False),
('{"device": "Device"}', 264, 'Device Used', 'Type of device used to access the internet (e.g., smartphone, computer)', 4, False, 0, 50, 1203, 219, 'deviceused', False),
('{"usage_hours": "Usage Hours"}', 265, 'Average Usage Hours', 'Average number of hours spent on the internet daily', 5, False, 0, 5, 1202, 219, 'usagehours', False),
('{"connection_type": "Connection Type"}', 266, 'Connection Type', 'Type of internet connection used (e.g., broadband, mobile data)', 6, False, 0, 30, 1203, 219, 'connectiontype', False),
('{"gender": "Gender"}', 267, 'Gender Distribution', 'Gender distribution of internet users', 7, False, 0, 10, 1203, 219, 'genderdistribution', False),
('{"income_level": "Income Level"}', 268, 'Income Level', 'Income level of users with internet access', 8, False, 0, 30, 1203, 219, 'incomelevel', False),
('{"education_level": "Education Level"}', 269, 'Education Level', 'Education level of internet users', 9, False, 0, 30, 1203, 219, 'educationlevel', False),
('{"year": "Year"}', 270, 'Year', 'Year in which internet usage data was collected', 10, False, 0, 4, 1202, 219, 'year', False);

INSERT INTO layout_fields (lyt_fld_tags, lyt_fld_id, lyt_fld_name, lyt_fld_desc, lyt_fld_order, lyt_fld_is_pk, lyt_fld_start, lyt_fld_length, lyt_fld_data_type_cd, lyt_id, lyt_fld_key, is_deleted) 
VALUES 
('{"region": "Region"}', 271, 'Region', 'Geographic region where population growth is measured', 1, False, 0, 50, 1203, 220, 'region', False),
('{"population_growth_rate": "Growth Rate"}', 272, 'Population Growth Rate', 'Annual population growth rate as a percentage', 2, False, 0, 10, 1202, 220, 'growthrate', False),
('{"total_population": "Total Population"}', 273, 'Total Population', 'Total population of the region', 3, False, 0, 10, 1202, 220, 'totalpopulation', False),
('{"urban_population": "Urban Population"}', 274, 'Urban Population Growth', 'Growth rate of the urban population', 4, False, 0, 10, 1202, 220, 'urbanpopulationgrowth', False),
('{"rural_population": "Rural Population"}', 275, 'Rural Population Growth', 'Growth rate of the rural population', 5, False, 0, 10, 1202, 220, 'ruralpopulationgrowth', False),
('{"age_distribution": "Age Distribution"}', 276, 'Age Distribution', 'Age group distribution within the population', 6, False, 0, 50, 1203, 220, 'agedistribution', False),
('{"birth_rate": "Birth Rate"}', 277, 'Birth Rate', 'Birth rate contributing to population growth', 7, False, 0, 10, 1202, 220, 'birthrate', False),
('{"death_rate": "Death Rate"}', 278, 'Death Rate', 'Death rate affecting population growth', 8, False, 0, 10, 1202, 220, 'deathrate', False),
('{"migration_rate": "Migration Rate"}', 279, 'Migration Rate', 'Rate of migration influencing population growth', 9, False, 0, 10, 1202, 220, 'migrationrate', False),
('{"year": "Year"}', 280, 'Year', 'Year for which population growth data is recorded', 10, False, 0, 4, 1202, 220, 'year', False);

