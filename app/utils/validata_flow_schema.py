import json
import jsonschema
from jsonschema import validate

from app.exceptions.flow import JsonNotValidError

schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
      "tasks": {
        "type": "array",
        "items": {
          "oneOf": [
            {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": ["SimpleHttpOperator"],
                  "description": "Type of the operator",
                  "ui_properties": {
                    "module_name": "Sensor",
                    "color": "#07A260",
                    "icon": "/assets/flow/Sensor.svg"
                  }
                },
                "task_id": {
                  "type": "string",
                  "description": "The task ID",
                  "ui_properties": {
                    "property_name": "Task Id",
                    "property_key": "task_id",
                    "ui_type": "text",
                    "order": 1,
                    "spancol": 1,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "http_conn_id": {
                  "type": "string",
                  "description": "The HTTP connection to run the operator against",
                  "ui_properties": {
                    "property_name": "Http conn. id",
                    "property_key": "http_conn_id",
                    "ui_type": "dropdown",
                    "order": 2,
                    "spancol": 1,
                    "mandatory": True,
                    "endpoint": "{catalog_base_url}/api/v1/environment/connections/{env_id}/http_connections",
                    "group_key": "property"
                  }
                },
                "endpoint": {
                  "type": "string",
                  "description": "The relative part of the full URL",
                  "ui_properties": {
                    "property_name": "Endpoint",
                    "property_key": "endpoint",
                    "ui_type": "text",
                    "order": 3,
                    "spancol": 1,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "method": {
                  "type": "string",
                  "enum": ["GET", "POST", "PUT"],
                  "description": "The HTTP method to use",
                  "ui_properties": {
                    "property_name": "Method",
                    "property_key": "method",
                    "ui_type": "enum",
                    "order": 4,
                    "spancol": 1,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "data": {
                  "type": "object",
                  "description": "The data to pass in the request",
                  "ui_properties": {
                    "property_name": "Data",
                    "property_key": "data",
                    "ui_type": "json",
                    "order": 5,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "property"
                  }
                },
                "headers": {
                  "type": "object",
                  "description": "The HTTP headers to be added to the request",
                  "ui_properties": {
                    "property_name": "Headers",
                    "property_key": "headers",
                    "ui_type": "json",
                    "order": 6,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "property"
                  }
                },
                "response_check": {
                  "type": "string",
                  "description": "A check against the 'requests' response object",
                  "ui_properties": {
                    "property_name": "Response check",
                    "property_key": "response_check",
                    "ui_type": "text",
                    "order": 7,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "response_filter": {
                  "type": "string",
                  "description": "A function allowing you to manipulate the response text",
                  "ui_properties": {
                    "property_name": "Response filter",
                    "property_key": "response_filter",
                    "ui_type": "text",
                    "order": 8,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "extra_options": {
                  "type": "object",
                  "description": "Extra options for the 'requests' library",
                  "ui_properties": {
                    "property_name": "Extra options",
                    "property_key": "extra_options",
                    "ui_type": "json",
                    "order": 9,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "log_response": {
                  "type": "boolean",
                  "description": "Log the response",
                  "ui_properties": {
                    "property_name": "Log response",
                    "property_key": "log_response",
                    "ui_type": "checkbox",
                    "order": 10,
                    "spancol": 1,
                    "mandatory": False,
                    "default": False,
                    "group_key": "settings"
                  }
                },
                "tcp_keep_alive": {
                  "type": "boolean",
                  "description": "Enable TCP Keep Alive for the connection",
                  "ui_properties": {
                    "property_name": "Tcp keep alive",
                    "property_key": "tcp_keep_alive",
                    "ui_type": "checkbox",
                    "order": 12,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "tcp_keep_alive_idle": {
                  "type": "integer",
                  "description": "The TCP Keep Alive Idle parameter",
                  "ui_properties": {
                    "property_name": "Tcp keep alive idle",
                    "property_key": "tcp_keep_alive_idle",
                    "ui_type": "number",
                    "order": 13,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "tcp_keep_alive_count": {
                  "type": "integer",
                  "description": "The TCP Keep Alive count parameter",
                  "ui_properties": {
                    "property_name": "Tcp keep alive count",
                    "property_key": "tcp_keep_alive_count",
                    "ui_type": "number",
                    "order": 14,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "tcp_keep_alive_interval": {
                  "type": "integer",
                  "description": "The TCP Keep Alive interval parameter",
                  "ui_properties": {
                    "property_name": "Tcp keep alive interval",
                    "property_key": "tcp_keep_alive_interval",
                    "ui_type": "number",
                    "order": 15,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "deferrable": {
                  "type": "boolean",
                  "description": "Run operator in the deferrable mode",
                  "ui_properties": {
                    "property_name": "Defferable",
                    "property_key": "deferrable",
                    "ui_type": "checkbox",
                    "order": 16,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "trigger_rule": {
                  "type": "string",
                  "enum": [
                    "all_success",
                    "all_failed",
                    "all_done",
                    "all_skipped",
                    "one_success",
                    "one_failed",
                    "one_done",
                    "none_failed",
                    "none_failed_min_one_success",
                    "none_skipped",
                    "always"
                  ],
                  "description": "The rule by which to trigger the task instance of the task",
                  "ui_properties": {
                    "property_name": "Trigger rule",
                    "property_key": "trigger_rule",
                    "ui_type": "enum",
                    "order": 17,
                    "spancol": 1,
                    "mandatory": True,
                    "default": "all_success",
                    "group_key": "property"
                  }
                },
                "depends_on": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "The task IDs that the current task depends on",
                  "ui_properties": {
                    "property_name": "Depends on",
                    "property_key": "depends_on",
                    "ui_type": "auto",
                    "order": 18,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "property"
                  }
                }
              },
              "required": [
                "type",
                "task_id",
                "http_conn_id",
                "endpoint",
                "method"
              ]
            },
            {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": ["HttpSensor"],
                  "description": "Type of the sensor",
                  "ui_properties": {
                    "module_name": "Sensor",
                    "color": "#07A260",
                    "icon": "/assets/flow/Sensor.svg"
                  }
                },
                "task_id": {
                  "type": "string",
                  "description": "The task ID",
                  "ui_properties": {
                    "property_name": "Task id",
                    "property_key": "task_id",
                    "ui_type": "text",
                    "order": 1,
                    "spancol": 1,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "http_conn_id": {
                  "type": "string",
                  "description": "The HTTP connection to run the sensor against",
                  "ui_properties": {
                    "property_name": "Http conn. id",
                    "property_key": "http_conn_id",
                    "ui_type": "dropdown",
                    "order": 2,
                    "spancol": 1,
                    "mandatory": True,
                    "endpoint": "{catalog_base_url}/api/v1/environment/connections/{env_id}/http_connections",
                    "group_key": "property"
                  }
                },
                "method": {
                  "type": "string",
                  "enum": ["GET", "POST"],
                  "description": "The HTTP request method to use",
                  "ui_properties": {
                    "property_name": "Method",
                    "property_key": "method",
                    "ui_type": "enum",
                    "order": 3,
                    "spancol": 1,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "endpoint": {
                  "type": "string",
                  "description": "The relative part of the full URL",
                  "ui_properties": {
                    "property_name": "Endpoint",
                    "property_key": "endpoint",
                    "ui_type": "text",
                    "order": 4,
                    "spancol": 1,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "request_params": {
                  "type": "object",
                  "description": "The parameters to be added to the GET URL",
                  "ui_properties": {
                    "property_name": "Request parameters",
                    "property_key": "request_params",
                    "ui_type": "json",
                    "order": 5,
                    "spancol": 1,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "headers": {
                  "type": "object",
                  "description": "The HTTP headers to be added to the GET request",
                  "ui_properties": {
                    "property_name": "Headers",
                    "property_key": "headers",
                    "ui_type": "json",
                    "order": 6,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "response_error_codes_allowlist": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "An allowlist to return False on poke(), not to raise exception",
                  "ui_properties": {
                    "property_name": "Request error codes allowlist",
                    "property_key": "response_error_codes_allowlist",
                    "ui_type": "list[string]",
                    "order": 7,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "response_check": {
                  "type": "string",
                  "description": "A check against the 'requests' response object",
                  "ui_properties": {
                    "property_name": "Response check",
                    "property_key": "response_check",
                    "ui_type": "text",
                    "order": 8,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "extra_options": {
                  "type": "object",
                  "description": "Extra options for the 'requests' library",
                  "ui_properties": {
                    "property_name": "Extra options",
                    "property_key": "extra_options",
                    "ui_type": "json",
                    "order": 9,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "tcp_keep_alive": {
                  "type": "boolean",
                  "description": "Enable TCP Keep Alive for the connection",
                  "ui_properties": {
                    "property_name": "Tcp keep alive",
                    "property_key": "tcp_keep_alive",
                    "ui_type": "checkbox",
                    "order": 10,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "tcp_keep_alive_idle": {
                  "type": "integer",
                  "description": "The TCP Keep Alive Idle parameter",
                  "ui_properties": {
                    "property_name": "Tcp keep alive idle",
                    "property_key": "tcp_keep_alive_idle",
                    "ui_type": "number",
                    "order": 11,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "tcp_keep_alive_count": {
                  "type": "integer",
                  "description": "The TCP Keep Alive count parameter",
                  "ui_properties": {
                    "property_name": "Tcp keep alive count",
                    "property_key": "tcp_keep_alive_count",
                    "ui_type": "number",
                    "order": 12,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "tcp_keep_alive_interval": {
                  "type": "integer",
                  "description": "The TCP Keep Alive interval parameter",
                  "ui_properties": {
                    "property_name": "Tcp keep alive interval",
                    "property_key": "tcp_keep_alive_interval",
                    "ui_type": "number",
                    "order": 13,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "trigger_rule": {
                  "type": "string",
                  "enum": [
                    "all_success",
                    "all_failed",
                    "all_done",
                    "all_skipped",
                    "one_success",
                    "one_failed",
                    "one_done",
                    "none_failed",
                    "none_failed_min_one_success",
                    "none_skipped",
                    "always"
                  ],
                  "description": "The rule by which to trigger the task instance of the task",
                  "ui_properties": {
                    "property_name": "Trigger rule",
                    "property_key": "trigger_rule",
                    "ui_type": "enum",
                    "order": 14,
                    "mandatory": True,
                    "default": "all_success",
                    "group_key": "property"
                  }
                },
                "depends_on": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "The task IDs that the current task depends on",
                  "ui_properties": {
                    "property_name": "Depends on",
                    "property_key": "depends_on",
                    "ui_type": "auto",
                    "order": 18,
                    "mandatory": False,
                    "group_key": "property"
                  }
                }
              },
              "required": [
                "type",
                "task_id",
                "http_conn_id",
                "method",
                "endpoint"
              ]
            },
            {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": ["BashOperator"],
                  "description": "Type of the operator",
                  "ui_properties": {
                    "module_name": "Custom",
                    "color": "#2B64D4",
                    "icon": "/assets/flow/Other.svg"
                  }
                },
                "task_id": {
                  "type": "string",
                  "description": "The task ID",
                  "ui_properties": {
                    "property_name": "Task id",
                    "property_key": "task_id",
                    "ui_type": "text",
                    "order": 1,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "bash_command": {
                  "type": "string",
                  "description": "The command, set of commands or reference to a bash script to be executed",
                  "ui_properties": {
                    "property_name": "Bash command",
                    "property_key": "bash_command",
                    "ui_type": "textbox",
                    "language": "shell",
                    "spancol": 2,
                    "order": 2,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "env": {
                  "type": "object",
                  "description": "Defines the environment variables for the new process",
                  "ui_properties": {
                    "property_name": "Environment variable",
                    "property_key": "env",
                    "ui_type": "json",
                    "order": 3,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "append_env": {
                  "type": "boolean",
                  "description": "If True, inherits the environment variables from current process",
                  "ui_properties": {
                    "property_name": "Append  environment",
                    "property_key": "append_env",
                    "ui_type": "checkbox",
                    "order": 4,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "output_encoding": {
                  "type": "string",
                  "description": "Output encoding of bash command",
                  "ui_properties": {
                    "property_name": "Output encoding",
                    "property_key": "output_encoding",
                    "ui_type": "text",
                    "order": 5,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "skip_on_exit_code": {
                  "type": "integer",
                  "description": "If task exits with this exit code, leave the task in 'skipped' state",
                  "ui_properties": {
                    "property_name": "Skip on exit code",
                    "property_key": "skip_on_exit_code",
                    "ui_type": "number",
                    "order": 6,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "cwd": {
                  "type": "string",
                  "description": "Working directory to execute the command in",
                  "ui_properties": {
                    "property_name": "Working directory",
                    "property_key": "cwd",
                    "ui_type": "text",
                    "order": 7,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "trigger_rule": {
                  "type": "string",
                  "enum": [
                    "all_success",
                    "all_failed",
                    "all_done",
                    "all_skipped",
                    "one_success",
                    "one_failed",
                    "one_done",
                    "none_failed",
                    "none_failed_min_one_success",
                    "none_skipped",
                    "always"
                  ],
                  "description": "The rule by which to trigger the task instance of the task",
                  "ui_properties": {
                    "property_name": "Trigger rule",
                    "property_key": "trigger_rule",
                    "ui_type": "enum",
                    "order": 8,
                    "mandatory": True,
                    "group_key": "property",
                    "default": "all_success"
                  }
                },
                "depends_on": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "The task IDs that the current task depends on",
                  "ui_properties": {
                    "property_name": "Depends on",
                    "property_key": "depends_on",
                    "ui_type": "auto",
                    "order": 9,
                    "group_key": "property",
                    "mandatory": False
                  }
                }
              },
              "required": ["type", "task_id", "bash_command"]
            },
            {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": ["EmailOperator"],
                  "description": "Type of the operator",
                  "ui_properties": {
                    "module_name": "Alert",
                    "color": "#C049C0",
                    "icon": "/assets/flow/Notify.svg"
                  }
                },
                "task_id": {
                  "type": "string",
                  "description": "The task ID",
                  "ui_properties": {
                    "property_name": "Task id",
                    "property_key": "task_id",
                    "ui_type": "text",
                    "order": 1,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "to": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "List of emails to send the email to",
                  "ui_properties": {
                    "property_name": "To",
                    "property_key": "to",
                    "ui_type": "list[emailids]",
                    "order": 2,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "subject": {
                  "type": "string",
                  "description": "Subject line for the email",
                  "ui_properties": {
                    "property_name": "Subject",
                    "property_key": "subject",
                    "ui_type": "text",
                    "order": 3,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "html_content": {
                  "type": "string",
                  "description": "Content of the email, HTML markup is allowed",
                  "ui_properties": {
                    "property_name": "Html content",
                    "property_key": "html_content",
                    "ui_type": "textbox",
                    "language": "plaintext",
                    "spancol": 2,
                    "order": 4,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "files": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "File names to attach in email",
                  "ui_properties": {
                    "property_name": "Files",
                    "property_key": "files",
                    "ui_type": "list[string]",
                    "order": 5,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "cc": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "List of recipients to be added in CC field",
                  "ui_properties": {
                    "property_name": "Cc",
                    "property_key": "cc",
                    "ui_type": "list[emailids]",
                    "order": 6,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "bcc": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "List of recipients to be added in BCC field",
                  "ui_properties": {
                    "property_name": "Bcc",
                    "property_key": "bcc",
                    "ui_type": "list[emailids]",
                    "order": 7,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "mime_subtype": {
                  "type": "string",
                  "description": "MIME sub content type",
                  "ui_properties": {
                    "property_name": "Mime subtype",
                    "property_key": "mime_subtype",
                    "ui_type": "text",
                    "order": 8,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "mime_charset": {
                  "type": "string",
                  "description": "Character set parameter added to the Content-Type header",
                  "ui_properties": {
                    "property_name": "Mime charset",
                    "property_key": "mime_charset",
                    "ui_type": "text",
                    "order": 9,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "custom_headers": {
                  "type": "object",
                  "description": "Additional headers to add to the MIME message",
                  "ui_properties": {
                    "property_name": "Custom headers",
                    "property_key": "custom_headers",
                    "ui_type": "json",
                    "order": 10,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "trigger_rule": {
                  "type": "string",
                  "enum": [
                    "all_success",
                    "all_failed",
                    "all_done",
                    "all_skipped",
                    "one_success",
                    "one_failed",
                    "one_done",
                    "none_failed",
                    "none_failed_min_one_success",
                    "none_skipped",
                    "always"
                  ],
                  "description": "The rule by which to trigger the task instance of the task",
                  "ui_properties": {
                    "property_name": "Trigger rule",
                    "property_key": "trigger_rule",
                    "ui_type": "enum",
                    "order": 11,
                    "mandatory": True,
                    "default": "all_success",
                    "group_key": "property"
                  }
                },
                "depends_on": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "The task IDs that the current task depends on",
                  "ui_properties": {
                    "property_name": "Depends on",
                    "property_key": "depends_on",
                    "ui_type": "auto",
                    "order": 12,
                    "mandatory": False,
                    "group_key": "property"
                  }
                }
              },
              "required": ["type", "task_id", "to", "subject", "html_content"]
            },
            {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": ["S3KeySensor"],
                  "description": "Type of the sensor",
                  "ui_properties": {
                    "module_name": "Sensor",
                    "color": "#07A260",
                    "icon": "/assets/flow/Sensor.svg"
                  }
                },
                "task_id": {
                  "type": "string",
                  "description": "The task ID",
                  "ui_properties": {
                    "property_name": "Task id",
                    "property_key": "task_id",
                    "ui_type": "text",
                    "order": 1,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "bucket_key": {
                  "type": "string",
                  "description": "The key(s) being waited on",
                  "ui_properties": {
                    "property_name": "Bucket key",
                    "property_key": "bucket_key",
                    "ui_type": "text",
                    "order": 2,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "bucket_name": {
                  "type": "string",
                  "description": "Name of the S3 bucket",
                  "ui_properties": {
                    "property_name": "Bucket name",
                    "property_key": "bucket_name",
                    "ui_type": "text",
                    "order": 3,
                    "mandatory": False,
                    "group_key": "property"
                  }
                },
                "wildcard_match": {
                  "type": "boolean",
                  "description": "Whether the bucket_key should be interpreted as a Unix wildcard pattern",
                  "ui_properties": {
                    "property_name": "Wildcard  match",
                    "property_key": "wildcard_match",
                    "ui_type": "checkbox",
                    "order": 4,
                    "mandatory": False,
                    "group_key": "property"
                  }
                },
                "check_fn": {
                  "type": "string",
                  "description": "Function that receives the list of the S3 objects with the context values, and returns a boolean",
                  "ui_properties": {
                    "property_name": "Check function",
                    "property_key": "check_fn",
                    "ui_type": "text",
                    "order": 5,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "aws_conn_id": {
                  "type": "string",
                  "description": "A reference to the S3 connection",
                  "ui_properties": {
                    "property_name": "Aws conn. id",
                    "property_key": "aws_conn_id",
                    "ui_type": "dropdown",
                    "order": 6,
                    "mandatory": True,
                    "endpoint": "{catalog_base_url}/api/v1/environment/connections/{env_id}/aws_connections",
                    "group_key": "property"
                  }
                },
                "verify": {
                  "type": "boolean",
                  "description": "Whether to verify SSL certificates for S3 connection",
                  "ui_properties": {
                    "property_name": "Verify  ssl",
                    "property_key": "verify",
                    "ui_type": "checkbox",
                    "order": 7,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "ver_CA":{
                  "type": "string",
                  "description": "A filename of the CA cert bundle to use",
                  "ui_properties": {
                      "property_name": "Ca cert bundle",
                      "property_key": "ca_verify",
                      "ui_type": "text",
                      "order": 8,
                      "mandatory": False
                  }
              },
                "deferrable": {
                  "type": "boolean",
                  "description": "Run operator in the deferrable mode",
                  "ui_properties": {
                    "property_name": "Deferrable",
                    "property_key": "deferrable",
                    "ui_type": "checkbox",
                    "order": 9,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "use_regex": {
                  "type": "boolean",
                  "description": "Whether to use regex to check bucket",
                  "ui_properties": {
                    "property_name": "Use regex",
                    "property_key": "use_regex",
                    "ui_type": "checkbox",
                    "order": 10,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "metadata_keys": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "List of head_object attributes to gather and send to check_fn",
                  "ui_properties": {
                    "property_name": "Metadata keys",
                    "property_key": "metadata_keys",
                    "ui_type": "list[string]",
                    "order": 11,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "trigger_rule": {
                  "type": "string",
                  "enum": [
                    "all_success",
                    "all_failed",
                    "all_done",
                    "all_skipped",
                    "one_success",
                    "one_failed",
                    "one_done",
                    "none_failed",
                    "none_failed_min_one_success",
                    "none_skipped",
                    "always"
                  ],
                  "description": "The rule by which to trigger the task instance of the task",
                  "ui_properties": {
                    "property_name": "Trigger rule",
                    "property_key": "trigger_rule",
                    "ui_type": "enum",
                    "order": 12,
                    "mandatory": True,
                    "default": "all_success",
                    "group_key": "property"
                  }
                },
                "depends_on": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "The task IDs that the current task depends on",
                  "ui_properties": {
                    "property_name": "Depends on",
                    "property_key": "depends_on",
                    "ui_type": "auto",
                    "order": 13,
                    "mandatory": False,
                    "group_key": "property"
                  }
                }
              },
              "required": ["type", "task_id", "bucket_key"]
            },
            {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": ["SFTPToS3Operator"],
                  "description": "Type of the operator",
                  "ui_properties": {
                    "module_name": "Transfer",
                    "color": "#8237E3",
                    "icon": "/assets/flow/Transfer.svg"
                  }
                },
                "task_id": {
                  "type": "string",
                  "description": "The task ID",
                  "ui_properties": {
                    "property_name": "Task id",
                    "property_key": "task_id",
                    "ui_type": "text",
                    "order": 1,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "sftp_conn_id": {
                  "type": "string",
                  "description": "The SFTP connection id for establishing a connection to the SFTP server",
                  "ui_properties": {
                    "property_name": "Sftp connection",
                    "property_key": "sftp_conn_id",
                    "ui_type": "dropdown",
                    "order": 2,
                    "mandatory": True,
                    "endpoint": "{catalog_base_url}/api/v1/environment/connections/{env_id}/sftp_connections",
                    "group_key": "property"
                  }
                },
                "sftp_path": {
                  "type": "string",
                  "description": "The SFTP remote path for downloading the file from the SFTP server",
                  "ui_properties": {
                    "property_name": "Sftp path",
                    "property_key": "sftp_path",
                    "ui_type": "text",
                    "order": 3,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "s3_conn_id": {
                  "type": "string",
                  "description": "The S3 connection id for establishing a connection to S3",
                  "ui_properties": {
                    "property_name": "S3 connection",
                    "property_key": "s3_conn_id",
                    "ui_type": "dropdown",
                    "order": 4,
                    "mandatory": True,
                    "endpoint": "{catalog_base_url}/api/v1/environment/connections/{env_id}/aws_connections",
                    "group_key": "property"
                  }
                },
                "s3_bucket": {
                  "type": "string",
                  "description": "The targeted S3 bucket to where the file is uploaded",
                  "ui_properties": {
                    "property_name": "Bucket NAME",
                    "property_key": "s3_bucket",
                    "ui_type": "text",
                    "order": 5,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "s3_key": {
                  "type": "string",
                  "description": "The targeted S3 key for uploading the file to S3",
                  "ui_properties": {
                    "property_name": "S3 file key",
                    "property_key": "s3_key",
                    "ui_type": "text",
                    "order": 6,
                    "mandatory": True,
                    "group_key": "property"
                  }
                },
                "use_temp_file": {
                  "type": "boolean",
                  "description": "If True, copies file first to local, if False streams file from SFTP to S3",
                  "ui_properties": {
                    "property_name": "Use temp file",
                    "property_key": "use_temp_file",
                    "ui_type": "checkbox",
                    "order": 7,
                    "mandatory": False,
                    "group_key": "settings"
                  }
                },
                "trigger_rule": {
                  "type": "string",
                  "enum": [
                    "all_success",
                    "all_failed",
                    "all_done",
                    "all_skipped",
                    "one_success",
                    "one_failed",
                    "one_done",
                    "none_failed",
                    "none_failed_min_one_success",
                    "none_skipped",
                    "always"
                  ],
                  "description": "The rule by which to trigger the task instance of the task",
                  "ui_properties": {
                    "property_name": "Trigger rule",
                    "property_key": "trigger_rule",
                    "ui_type": "enum",
                    "order": 8,
                    "mandatory": True,
                    "default": "all_success",
                    "group_key": "property"
                  },
                  "depends_on": {
                    "type": "array",
                    "items": {
                      "type": "string"
                    },
                    "description": "The task IDs that the current task depends on",
                    "ui_properties": {
                      "property_name": "Depends on",
                      "property_key": "depends_on",
                      "ui_type": "auto",
                      "order": 9,
                      "mandatory": False,
                      "group_key": "property"
                    }
                  }
                }
              },
              "required": [
                "type",
                "task_id",
                "sftp_conn_id",
                "sftp_path",
                "s3_conn_id",
                "s3_bucket",
                "s3_key"
              ]
            }
          ]
        }
      }
    },
    "required": ["tasks"]
  }
  

def validate_json(data):
    try:    
        json_data = json.loads(data) # convert string to json
        validate(instance=json_data, schema=schema) # validate json against schema
    except jsonschema.exceptions.ValidationError as err:
        raise JsonNotValidError(
            context={"error":err}
        )
