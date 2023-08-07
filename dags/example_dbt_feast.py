"""
This dag runs a dbt task group via the cosmos provider
on feast sample data stored in a local postgres container 

Then the dag runs feast materialize to move features 
into a online store in the same postgres, finally 
get_online_features retrieves features from that online store
"""
from airflow.decorators import dag, task
from cosmos.providers.dbt.task_group import DbtTaskGroup
from feast import FeatureStore

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

FEAST_PATH = "/usr/local/airflow/"
feature_store = FeatureStore("/usr/local/airflow/include/")

@dag(
    start_date=datetime(2023, 6, 1),
    schedule=None,
    catchup=False,
)
def dbt_feast_dag():
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

    @task(task_id="feast_materialize")
    def feast_materialize():
        feature_store.materialize_incremental(end_date=now().subtract(minutes=5))

    @task(task_id="get_online_features")
    def feast_get_online_features(feature_service, entity_rows):
        service = feature_store.get_feature_service(feature_service)
        features = feature_store.get_online_features(
            features=service,
            entity_rows=entity_rows
        ).to_dict()

        print(features)
    dbt >> feast_materialize() >> feast_get_online_features(feature_service="driver_activity", entity_rows=[{"driver_id": 1004},{"driver_id": 1005},])
    
dbt_feast_dag()
