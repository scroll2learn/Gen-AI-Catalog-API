from abc import ABC, abstractmethod

class AirflowService(ABC):

    @abstractmethod
    async def list_environments(self):
        pass

    @abstractmethod
    async def get_environment_by_name(self):
        pass

    @abstractmethod
    async def list_dags(self):
        pass

    @abstractmethod
    async def trigger_dag(self):
        pass

    @abstractmethod
    async def get_dag_status(self):
        pass

    @abstractmethod
    async def get_dag_last_parsed_time(self):
        pass

    @abstractmethod
    async def get_airflow_connections_list(self):
        pass

    @abstractmethod
    async def get_airflow_connection_by_id(self):
        pass
