"""
This dag runs a dbt task group via the cosmos provider
on feast sample data stored in a local postgres container 
"""

from airflow.decorators import dag, task
from cosmos.providers.dbt.task_group import DbtTaskGroup

from pendulum import datetime, now

CONNECTION_ID = "postgres"
DB_NAME = "postgres"
SCHEMA_NAME = "public"
DBT_PROJECT_NAME = "dbt-feast"
# the path where Cosmos will find the dbt executable
# in the virtual environment created in the Dockerfile
DBT_EXECUTABLE_PATH = "/usr/local/airflow/dbt_venv/bin/dbt"
# The path to your dbt root directory
DBT_ROOT_PATH = "/usr/local/airflow/dags/dbt"

@dag(
    start_date=datetime(2023, 6, 1),
    schedule=None,
    catchup=False,
)
def dbt_dag():
    dbt = DbtTaskGroup(
        group_id="transform_data",
        dbt_project_name=DBT_PROJECT_NAME,
        conn_id=CONNECTION_ID,
        dbt_root_path=DBT_ROOT_PATH,
        dbt_args={
            "dbt_executable_path": DBT_EXECUTABLE_PATH,
            "schema": SCHEMA_NAME,
        },
    )

    dbt
    
dbt_dag()
