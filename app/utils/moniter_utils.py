from typing import Optional
from app.core.config import Config
import httpx
from fastapi import HTTPException
from datetime import datetime

from app.models import bh_project

FAILED_JOB_SQL_TEMPLATE = "SELECT * FROM auditdb.bh_job_details WHERE flow_status={flow_status}"
IN_PROGRESS_JOB_SQL_TEMPLATE = "SELECT * FROM auditdb.bh_job_details WHERE flow_status='{flow_status}' AND job_start_time < NOW() - INTERVAL '{hours} hours'"

def store_monitor_data(flow_id: int, project_id: int, bh_project_name: Optional[str], alert_settings: dict, username: str, flow_key: str):
    
    monitor_data_list = []
    current_time = datetime.utcnow().isoformat() + "Z"

    # Mapping of alert setting to status and template names
    status_mapping = {
        "on_job_start": {"flow_status": "Started", "monitor_type": "information", "monitor_template_id":3},
        "on_job_failure": {"flow_status": "Failed", "monitor_type": "action", "monitor_template_id":2},
        "on_job_success": {"flow_status": "Success", "monitor_type": "information", "monitor_template_id":1},
        "long_running": {
            "flow_status": "In Progress",
            "hours": 2,
            "monitor_type": "action",
            "monitor_template_id":4
        }
    }
    for setting, enabled in alert_settings.items():
        if enabled:
            status = status_mapping.get(setting)
            if not status:
                continue  # Skip unknown settings

            
            monitor_data = {
                "input_parameters": {},
                "tags": {},
                "flow_id": flow_id,
                "flow_name": flow_key,
                "flow_key": flow_key,
                "flow_status": status["flow_status"],
                "monitor_template_id": status["monitor_template_id"],
                "project_id": str(project_id),
                "project_name": bh_project_name,
                "monitor_description": f"{flow_key}-{status['monitor_type']}",
                "monitor_type": status["monitor_type"],
                "status": "active",
                "created_by": username,
                "updated_by": "None",
                "created_on": current_time,
                "updated_on": current_time,
            }


            # Set specific input parameters for 'in progress' jobs
            if setting == "long_running":
                monitor_data["input_parameters"] = {
                    "flow_key": flow_key,
                    "flow_status": status["flow_status"],
                    "hours": status["hours"]
                }
            else:
                monitor_data["input_parameters"] = {
                    "flow_key": flow_key,
                    "flow_status": status["flow_status"]
                }

            monitor_data_list.append(monitor_data)

    return monitor_data_list


async def request_create_monitor(monitor_data: dict):
    async with httpx.AsyncClient() as client:
        try:
            cfg = Config()
            response = await client.post(cfg.BH_MONITER_URL, json=monitor_data)
            response.raise_for_status()  # Check for errors
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error creating monitor: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error connecting to the monitor API: {str(e)}"
            )
    return response.json()
