INSERT INTO bh_project (
    tags, bh_project_id, bh_project_name, bh_github_provider, bh_github_email, 
    bh_default_branch, bh_github_url, status, ytd_cost, current_month_cost, 
    total_storage, bh_github_username, is_deleted
) VALUES
    ('{"education":"student"}', 1001, 'Education', 4100, 'johndoe@bighammer.ai', 'main', 'https://github.com/john-deo/education', 'active', 0, 0, 0, 'john-doe', False),
    ('{"public":"health"}', 1002, 'Public', 4100, 'johndoe@bighammer.ai', 'main', 'https://github.com/john-deo/public', 'active', 0, 0, 0, 'john-doe', False),
    ('{"transport":"public"}', 1003, 'Transport', 4100, 'janedoe@bighammer.ai', 'main', 'https://github.com/jane-deo/transport', 'active', 0, 0, 0, 'jane-doe', False),
    ('{"env":"climate"}', 1004, 'Environment', 4100, 'johndoe@bighammer.ai', 'main', 'https://github.com/john-deo/env', 'active', 0, 0, 0, 'john-doe', False);

INSERT INTO project_environment (
    tags, bh_env_id, bh_env_name, bh_env_provider, cloud_provider_cd, 
    cloud_region_cd, status
) VALUES 
    ('{"aws":"dev"}', 1001, 'AWS Development', 301, 101, 1, 'active'),
    ('{"aws":"qa"}', 1002, 'AWS QA', 304, 101, 1, 'active'),
    ('{"aws":"production"}', 1003, 'AWS Production', 305, 101, 1, 'active'),
    ('{"gcp":"dev"}', 1004, 'GCP Development', 301, 102, 1, 'active'),
    ('{"gcp":"qa"}', 1005, 'GCP QA', 304, 102, 1, 'active'),
    ('{"gcp":"production"}', 1006, 'GCP Production', 305, 102, 1, 'active');



INSERT INTO flow (tags, flow_id, flow_name, bh_project_id, notes, flow_key, status, alert_settings, recipient_email) VALUES 
('{"tagList":[{"hospital":"montly_report"}]}', 1001, 'Hospital facilities Monthly', 1002, 'this flow maintain the monthly report of hospital facilities', 'hospital_facilities_monthly', 'active', '{"on_job_start": true, "on_job_failure": true, "on_job_success": false, "long_running": false}', '{"email": ["info@bighammer.ai"]}'),
('{"tagList":[{"hospital":"weekly_report"}]}', 1002, 'Hospital facilities Weekly', 1002, 'this flow maintain the weekly report of hospital facilities', 'hospital_facilities_weekly', 'active', '{"on_job_start": true, "on_job_failure": true, "on_job_success": false, "long_running": false}', '{"email": ["info@bighammer.ai"]}'),
('{"tagList":[{"hospital":"daily_report"}]}', 1003, 'Hospital facilities Daily', 1002, 'this flow maintain the daily report of hospital facilities', 'hospital_facilities_daily', 'active', '{"on_job_start": true, "on_job_failure": true, "on_job_success": false, "long_running": false}', '{"email": ["info@bighammer.ai"]}'),
('{"tagList":[{"road_condition":"monthly"}]}', 1004, 'Road Condition Monthly', 1003, 'This flow maintian the report for Montly Road condition', 'road_condition_monthly', 'active', '{"on_job_start": true, "on_job_failure": true, "on_job_success": false, "long_running": false}', '{"email": ["info@bighammer.ai"]}'),
('{"tagList":[{"road_condition":"weekly"}]}', 1005, 'Road Condition Weekly', 1003, 'This flow maintian the report for Weekly Road condition', 'road_condition_weekly', 'active', '{"on_job_start": true, "on_job_failure": true, "on_job_success": false, "long_running": false}', '{"email": ["info@bighammer.ai"]}'),
('{"tagList":[{"road_condition":"daily"}]}', 1006, 'Road Condition Daily', 1003, 'This flow maintian the report for Daily Road condition', 'road_condition_daily', 'active', '{"on_job_start": true, "on_job_failure": true, "on_job_success": false, "long_running": false}', '{"email": ["info@bighammer.ai"]}'),
('{"tagList":[{"env":"Climate"}]}', 1007, 'Environment Climate Monthly', 1004, 'This a flow maintain a monthly report of env climate data', 'environment_climate_monthly', 'active', '{"on_job_start": true, "on_job_failure": true, "on_job_success": false, "long_running": false}', '{"email": ["info@bighammer.ai"]}'),
('{"tagList":[{"env":"Climate"}]}', 1008, 'Environment Climate Weekly', 1004, 'This a flow maintain a weekly report of env climate data', 'environment_climate_weekly', 'active', '{"on_job_start": true, "on_job_failure": true, "on_job_success": false, "long_running": false}', '{"email": ["info@bighammer.ai"]}'),
('{"tagList":[{"env":"Climate"}]}', 1009, 'Environment Climate Daily', 1004, 'This a flow maintain a daily report of env climate data', 'environment_climate_daily', 'active', '{"on_job_start": true, "on_job_failure": true, "on_job_success": false, "long_running": false}', '{"email": ["info@bighammer.ai"]}'),
('{"tagList":[{"school":"data"}]}', 1010, 'School Enrollment Year', 1001, 'This flow contain the year of school enrollment', 'school_enrollment', 'active', '{"on_job_start": true, "on_job_failure": true, "on_job_success": false, "long_running": false}', '{"email": ["info@bighammer.ai"]}');

INSERT INTO pipeline (pipeline_name, pipeline_key, bh_project_id, pipeline_id, status) VALUES 
('Hospital facilities Monthly', 'hospital_facilities_monthly', 1002, 1001, 'active'),
('Hospital facilities Weekly', 'hospital_facilities_weekly', 1002, 1002, 'active'),
('Hospital facilities Daily', 'hospital_facilities_daily', 1002, 1003, 'active'),
('Road Condition Monthly', 'road_condition_monthly', 1003, 1004, 'active'),
('Road Condition Weekly', 'road_condition_weekly', 1003, 1005, 'active'),
('Road Condition Daily', 'road_condition_daily', 1003, 1006, 'active'),
('Environment Climate Monthly', 'environment_climate_monthly', 1004, 1007, 'active'),
('Environment Climate Weekly', 'environment_climate_weekly', 1004, 1008, 'active'),
('Environment Climate Daily', 'environment_climate_daily', 1004, 1009, 'active'),
('School Enrollment Year', 'school_enrollment', 1001, 1010, 'active');


update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=1;
update catalogdb.data_source SET bh_project_id = 1004 where data_src_id=2;
update catalogdb.data_source SET bh_project_id = 1003 where data_src_id=3;
update catalogdb.data_source SET bh_project_id = 1004 where data_src_id=4;
update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=5;
update catalogdb.data_source SET bh_project_id = 1001 where data_src_id=6;
update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=7;
update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=8;
update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=9;
update catalogdb.data_source SET bh_project_id = 1003 where data_src_id=10;
update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=11;
update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=12;
update catalogdb.data_source SET bh_project_id = 1004 where data_src_id=13;
update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=14;
update catalogdb.data_source SET bh_project_id = 1003 where data_src_id=15;
update catalogdb.data_source SET bh_project_id = 1003 where data_src_id=16;
update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=17;
update catalogdb.data_source SET bh_project_id = 1001 where data_src_id=18;
update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=19;
update catalogdb.data_source SET bh_project_id = 1002 where data_src_id=20;


