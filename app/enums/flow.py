from enum import Enum

class IntervalType(str, Enum):
    MINUTES = "minutes"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class AlertType(str, Enum):
    JOB_START = "on_job_start"
    JOB_FAILURE = "on_job_failure"
    JOB_SUCCESS = "on_job_success"

class SchemaTypes(str, Enum):
    FLOW = "flow"
    PIPELINE = "pipeline"
    CONNECTIONS = "connections"
