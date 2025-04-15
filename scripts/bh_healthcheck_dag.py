from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

def print_hello():
    return 'Health Check Dag from BH'

# Create the DAG
dag = DAG(
    'bh_healthcheck_dag',
    description='Health Check Dag',
    schedule_interval='0 12 * * *',  # Set your desired schedule here
    start_date=datetime(2017, 3, 20),  # Choose an appropriate start date
    catchup=False  # Disable backfilling for simplicity
)

# Define a PythonOperator task that runs our print_hello function
healthcheck_operator = PythonOperator(
    task_id='healthcheck_task',
    python_callable=print_hello,
    dag=dag
)

# You can add more tasks here if needed!

# Set up the task dependencies
healthcheck_operator

# Save this code as hello_world.py in your AIRFLOW_HOME/dags directory.
