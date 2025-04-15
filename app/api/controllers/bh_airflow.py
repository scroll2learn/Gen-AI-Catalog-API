import logging
from typing import List, Optional


from app.api.deps import get_context
from app.core.context import Context
from app.exceptions.bh_project import DecryptExceptionError
from app.services.aes import decrypt_string
from app.utils.cloud_service_utils import get_cloud_decrypted_secrets
from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app.utils.auth_wrapper import authorize
from app.core.config import Config

from app.utils.airflow_utils.airflow_factory import AirflowFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/list-airflow-environments",
    status_code=http_status.HTTP_200_OK,
)
async def list_airflow_environments(
    *,
    bh_env_name: str,
    location: str = "us-east-1",
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    Endpoint to get Airflow environment details.

    Args:
        env_name: Environment name of the client.
        authorized: Authorization dependency.

    Returns:
        A list of Airflow environments available in AWS/GCP projects.
    """ 
    
    if authorized:
        cfg = Config()
        airflow_service = await AirflowFactory.get_airflow_service(cfg.CLOUD_TYPE, bh_env_name, ctx, location)
        response = await airflow_service.list_environments()
    else:
        response = {"error": "Unauthorized access."}
    return response


@router.get(
    "/get_airflow_environment",
    status_code=http_status.HTTP_200_OK,
)
async def get_airflow_environment(
    *,
    airflow_env_name: str,
    bh_env_name: str,
    ctx: Context = Depends(get_context),
    location: str = "us-east-1",
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    To get airflow environment details.

    Args:
        airflow_env_name: The name of the Airflow environment.
        authorized: Authorization dependency.

    Returns:
        A success status and Airflow environment details.
    """    
    if authorized:
        cfg = Config()
        airflow_service = await AirflowFactory.get_airflow_service(cfg.CLOUD_TYPE, bh_env_name, ctx, location)
        response = await airflow_service.get_environment_by_name(airflow_env_name)
    else:
        response = {"error": "Unauthorized access."}
    return response

@router.get(
    "/dag_parse_time",
    status_code=http_status.HTTP_200_OK,
)
async def dag_parse_time(
    dag_id: str,
    bh_env_name: str,
    airflow_env_name: str = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    To get the last parsed time of a DAG.

    Args:
        airflow_env_name: The name of the Airflow environment.
        authorized: Authorization dependency.

    Returns:
        A success status and the last parsed time of a DAG.
    """
    if authorized:
        cfg = Config()
        airflow_service = await AirflowFactory.get_airflow_service(cfg.CLOUD_TYPE, bh_env_name, ctx, airflow_env_name)
        # response = await airflow_service.make_api_call(f'/api/v1/dags/{dag_id}?fields=last_parsed_time', method='GET')
        response = await airflow_service.get_dag_last_parsed_time(dag_id=dag_id)
    else:
        response = {"error": "Unauthorized access."}
    return response


@router.post(
    "/trigger_dag",
    status_code=http_status.HTTP_200_OK,
)
async def trigger_dag(
    bh_env_name: str,
    dag_id: str,
    airflow_env_name: str = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    To trigger a DAG.

    Args:
        airflow_env_name: The name of the Airflow environment.
        authorized: Authorization dependency.

    Returns:
        A success status and the response of the DAG trigger.
    """
    if authorized:
        cfg = Config()
        airflow_service = await AirflowFactory.get_airflow_service(cfg.CLOUD_TYPE, bh_env_name, ctx, airflow_env_name)
        # response = await airflow_service.make_api_call(f'/api/v1/dags/{dag_id}/dagRuns', method='POST', json={})
        response = await airflow_service.trigger_dag(dag_id=dag_id)
    else:
        response = {"error": "Unauthorized access."}
    return response


@router.get(
    "/dag_status",
    status_code=http_status.HTTP_200_OK,
)
async def dag_status(
    bh_env_name: str,
    dag_id: str,
    dag_run_id: str,
    airflow_env_name: str = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    To get the status of a DAG.

    Args:
        airflow_env_name: The name of the Airflow environment.
        authorized: Authorization dependency.

    Returns:
        A success status and the status of a DAG.
    """
    if authorized:
        cfg = Config()
        airflow_service = await AirflowFactory.get_airflow_service(cfg.CLOUD_TYPE, bh_env_name, ctx, airflow_env_name)
        response = await airflow_service.get_dag_status(dag_id=dag_id, dag_run_id=dag_run_id)
    else:
        response = {"error": "Unauthorized access."}
    return response


@router.get(
    "/get_dag_logs",
    status_code=http_status.HTTP_200_OK,
)
async def dag_runs(
    dag_id: str,
    dag_run_id: str,
    task_id: str,
    bh_env_name: str,
    airflow_env_name: str = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    To get the DAG logs of a DAG.
    """
    if authorized:
        cfg = Config()
        airflow_service = await AirflowFactory.get_airflow_service(cfg.CLOUD_TYPE, bh_env_name, ctx, airflow_env_name)
        response = await airflow_service.get_airflow_task_logs(dag_id=dag_id, dag_run_id=dag_run_id, task_id=task_id)
    else:
        response = {"error": "Unauthorized access."}
    return response


@router.get(
    "/get_dag_task_id",
    status_code=http_status.HTTP_200_OK,
)
async def get_dag_task_id(
    dag_id: str,
    dag_run_id: str,
    bh_env_name: str,
    airflow_env_name: str = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    To get the DAG tasks of a DAG.
    """
    if authorized:
        cfg = Config()
        airflow_service = await AirflowFactory.get_airflow_service(cfg.CLOUD_TYPE, bh_env_name, ctx, airflow_env_name)
        response = await airflow_service.get_airflow_task_id(dag_id=dag_id, dag_run_id=dag_run_id)
    else:
        response = {"error": "Unauthorized access."}
    return response

@router.get(
    "/get-connection-list/",
    status_code=http_status.HTTP_200_OK,
)
async def get_connection_list(
    bh_env_name: str,
    airflow_env_name: str = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    To get list of connections
    """
    if authorized:
        cfg = Config()
        airflow_service = await AirflowFactory.get_airflow_service(cfg.CLOUD_TYPE, bh_env_name, ctx, airflow_env_name)
        response = await airflow_service.get_airflow_connections_list()
    else:
        response = {"error": "Unauthorized access."}
    return response


@router.get(
    "/get-connection-by-id/",
    status_code=http_status.HTTP_200_OK,
)
async def get_connection_by_id(
    bh_env_name: str,
    airflow_env_name: str = None,
    connection_id: str = None,
    ctx: Context = Depends(get_context),
    authorized: Optional[dict] = Depends(authorize('admin_module', 'edit'))
):
    """
    To get the connection by id
    """
    if authorized:
        cfg = Config()
        airflow_service = await AirflowFactory.get_airflow_service(cfg.CLOUD_TYPE, bh_env_name, ctx, airflow_env_name)
        response = await airflow_service.get_airflow_connection_by_id(connection_id)
    else:
        response = {"error": "Unauthorized access."}
    return response
