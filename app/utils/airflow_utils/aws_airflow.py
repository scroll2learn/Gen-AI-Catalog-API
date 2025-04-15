import boto3
import logging
import time
from app.utils.airflow_utils.airflow_services import AirflowService

from botocore.exceptions import ClientError
import requests
from urllib.parse import urljoin
from app.exceptions.airflow import AirflowException


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AWSAirflowService(AirflowService):

    def __init__(
        self, access_key, secret_access_key, region_name: str, environment_name=None
    ):
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.region_name = region_name
        self.environment_name = environment_name

        # Create a boto3 session
        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
        )

        # Create an Airflow session
        self.airflow_session = self.session.client("mwaa")


    async def list_environments(self) -> list[str]:
        """
        List all MWAA environments in the account and region.

        :return: List of environment names.
        """
        try:
            response = self.airflow_session.list_environments()
            environments = response.get("Environments", [])
            logger.info(f"Retrieved MWAA environments: {environments}")
            return environments
        except ClientError as e:
            logger.error(f"Failed to list MWAA environments: {e}")
            raise

    async def get_environment_by_name(self, environment_name) -> dict:
        """
        Retrieve details for a specific MWAA environment.

        :param environment_name: Name of the MWAA environment.
        :return: Dictionary containing environment details.
        """
        try:
            response = self.airflow_session.get_environment(Name=environment_name)
            environment_details = response.get("Environment", {})
            logger.info(
                f"Retrieved details for environment '{environment_name}': {environment_details}"
            )
            return environment_details
        except ClientError as e:
            logger.error(
                f"Failed to get details for environment '{environment_name}': {e}"
            )
            raise

    async def list_dags(self):
        try:
            if self.environment_name:
                request_params = {
                    "Name": self.environment_name,
                    "Path": "/dags",
                    "Method": "GET",
                    "QueryParameters": {"paused": "false"},
                }
                response = self.airflow_session.invoke_rest_api(**request_params)
                return response
        except Exception as e:
            logger.error(f"Failed to make API call: {e}")
            raise AirflowException(context={"message": str(e)})

    async def trigger_dag(self, dag_id: str, conf: dict = {}, dag_run_id: str = None):
        try:
            if self.environment_name:
                if not dag_run_id:
                    dag_run_id = f"bh__{int(time.time())}"
                if not conf:
                    conf = {}
                request_params = {
                    "Name": self.environment_name,
                    "Path": f"/dags/{dag_id}/dagRuns",
                    "Method": "POST",
                    "Body": {"conf": conf, "dag_run_id": dag_run_id},
                }
                response = self.airflow_session.invoke_rest_api(**request_params)
                if response["RestApiStatusCode"] == 200:
                    return response["RestApiResponse"]
                return response
        except Exception as e:
            logger.error(f"Failed to make API call: {e}")
            raise AirflowException(context={"message": str(e)})

    async def get_dag_status(self, dag_id: str, dag_run_id: str):
        try:
            if self.environment_name:
                request_params = {
                    "Name": self.environment_name,
                    "Path": f"/dags/{dag_id}/dagRuns/{dag_run_id}",
                    "Method": "GET",
                }
                response = self.airflow_session.invoke_rest_api(**request_params)
                return response
        except Exception as e:
            logger.error(f"Failed to make API call: {e}")
            raise AirflowException(context={"message": str(e)})

    async def get_dag_last_parsed_time(self, dag_id: str):
        try:
            if self.environment_name:
                request_params = {
                    "Name": self.environment_name,
                    "Path": f"/dags/{dag_id}",
                    "Method": "GET",
                }
                response = self.airflow_session.invoke_rest_api(**request_params)
                return response["RestApiResponse"]["last_parsed_time"]
        except Exception as e:
            logger.error(f"Failed to make API call: {e}")
            return None


    async def get_airflow_task_logs(self, dag_id: str, dag_run_id: str, task_id: str):
        try:
            if self.environment_name:
                request_params = {
                    "Name": self.environment_name,
                    "Path": f"/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/1?full_content=false",
                    "Method": "GET",
                }
                response = self.airflow_session.invoke_rest_api(**request_params)
                if response["RestApiStatusCode"] == 200:
                    return response["RestApiResponse"]
                return response
        except Exception as e:
            logger.error(f"Failed to make API call: {e}")
            raise AirflowException(context={"message": str(e)})

    async def get_airflow_task_id(self, dag_id: str, dag_run_id: str):
        try:
            if self.environment_name:
                request_params = {
                    "Name": self.environment_name,
                    "Path": f"/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances",
                    "Method": "GET",
                }
                response = self.airflow_session.invoke_rest_api(**request_params)
                if response["RestApiStatusCode"] == 200:
                    return response["RestApiResponse"]
                return response
        except Exception as e:
            logger.error(f"Failed to make API call: {e}")
            raise AirflowException(context={"message": str(e)})

    async def get_airflow_connections_list(self):
        try:
            if self.environment_name:
                request_params = {
                    "Name": self.environment_name,
                    "Path": f"/connections",
                    "Method": "GET",
                }
                response = self.airflow_session.invoke_rest_api(**request_params)
                if response["RestApiStatusCode"] == 200:
                    return response["RestApiResponse"]
                return response
        except Exception as e:
            logger.error(f"Failed to make API call: {e}")
            raise AirflowException(context={"message": str(e)})
    
    async def get_airflow_connection_by_id(self, connection_id):
        try:
            if self.environment_name:
                request_params = {
                    "Name": self.environment_name,
                    "Path": f"/connections/{connection_id}",
                    "Method": "GET",
                }
                response = self.airflow_session.invoke_rest_api(**request_params)
                if response["RestApiStatusCode"] == 200:
                    return response["RestApiResponse"]
                return response
        except Exception as e:
            logger.error(f"Failed to make API call: {e}")
            raise AirflowException(context={"message": str(e)})