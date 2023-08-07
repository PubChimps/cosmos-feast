# Orchestrating a feature store with dbt, feast and Astronomer Cosmos


## Prereqs
[Homebrew](https://brew.sh/)

[Docker](https://docs.docker.com/desktop/install/mac-install/)

## Install Astronomer CLI
The Astro CLI is a command line interface that makes it easy to get started with Apache Airflow, where will be orchestrating dbt and feast together in data pipelines called DAGs. Many other data and cloud services can be easily added to this example DAG, or run as separate DAGs, via the [Astronomer Registry](https://registry.astronomer.io/)

```
brew install astro
mkdir astro && cd astro
astro dev init
```

## Adding Cosmos and Feast to Astronomer
In the `astro` directory that was automatically created, edit the `Dockerfile` to include the command below:

```
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
pip install --no-cache-dir dbt-postgres && deactivate
```

Add the following to `requirements.txt`
```
astronomer-cosmos==0.6.8
feast[postgres]
```
### Adding dbt models 
```
cd dags
mkdir dbt && cd dbt
```

Add the `dbt_feast` directory in this repo to `astro/dags/dbt/`

### Start Astronomer
Astronomer will automatically create the docker images needed to run Airflow, including the Postgres db we will use with Feast and dbt... run
```
astro dev start
```
This should finish with the creation of an Astronomer Web UI, accessable [here](http://localhost:8080/)

### Feast Init
Feast and dbt are going to utilize the postgres database that Astronomer is using to maintain Airflow metadata. To begin setting up feast to do so, run the command below and answer its prompts.

```
feast init -t postgres
```
Keep all the postgres config options as default, with `Postgres user:` as `postgres` and `Postgres password:` as `postgres`.

Type `Y` when Feast asks `Should I upload example data to Postgres (overwriting "feast_driver_hourly_stats" table)?`

Note the directory Feast creates (mine was called ***`crack_possum`***).

### Run example_dbt
Place [example_dbt.py](./dags/example_dbt.py) from this repo in the `dags` directory that `astro dev init` created. This example dag will run the dbt models that were set up earlier with the a dbt_profile that reuses the postgres db Airflow is using for metadata. To allow Airflow DAGs to use this database as well, we will have to set an Airflow Connection.

In the Astro UI, go to Admin, then Connections, then [Add a new record](http://localhost:8080/connection/add). 

The new Connection will have the following information:
 * Connection Id - `postgres`
 * Connection Type - Postgres
 * Description
 * Host - `postgres`
 * Schema - `postgres`
 * Login - `postgres`
 * Password - `postgres`
 * Port - `5432`
You can then `Test` the new Connection to ensure the "Connection successfully tested" and `Save the new Connection`.

In the DAGs section of the Astro UI, you should see the `example_dbt` DAG that was added previously, trigger it to start running by clicking the play button on its page.

### Add feast to example 
Feast will take the transformations the dbt creates and move them to an offline store for machine learning model training and an online store to serve models in production. To do so replace the example_repo.py that feast generated with the [example](./example_repo.py) from this guide, then run `feast apply`

```
cd crack_possum # change to whatever name feast gave
cd feature_repo
rm example_repo.py # replace with example_repo from this guide
```

```
feast apply
```

With the features now defined in a feature store, we can materialize them in Airflow. Materialization in feast moves data from an offline store to an online store in order to serve the latest features to models for online prediction. To do so with Airflow, first add this guide's [feature_store.yaml](./feature_store.yaml) into Astro's `include/` directory. Then add this guide's [example_dbt_feast.py](./dags/example_dbt_feast.py) to Astro's `dags/` directory.

Then select the newly added DAG and trigger it. You should be able to see the output of Feast materialization and get_online_features tasks.




