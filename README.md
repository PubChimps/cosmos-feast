# cosmos-feast

## Table of Contents
### Prereqs
### Astronomer CLI

## Prereqs
[Homebrew](https://brew.sh/)
[Docker](https://docs.docker.com/desktop/install/mac-install/)

## Astronomer CLI
The Astro CLI is a command line interface that makes it easy to get started with Apache Airflow, where will be orchestrating dbt and feast together in data pipelines called DAGs. Many other data and cloud services can be easily added to this example DAG, or run as separate DAGs, via the Astronomer Registry

### Install Astronomer CLI
```
brew install astro
mkdir astro && cd astro
astro dev init
```

### Adding Cosmos and Feast to Astronomer
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
#### Adding dbt models 
```
cd dags
mkdir dbt && cd dbt
```

Add the `dbt_feast directory` in this repo to ~/astro/dags/dbt/

#### Adding dbt models 
Add `example_cosmos_feast.py` in this repo to ~/astro/dags/

#### Start Astronomer
Astronomer will automatically create the docker images needed to run Airflow, including the Postgres db we will use with Feast and dbt... run
```
astro dev start
```
#### Feast Setup
Run
```
cd include
feast init -t postgres
```
Keep all the postgres config options as default, with `Postgres user:` as `postgres` and `Postgres password:` as `postgres`.

Type `Y` when Feast asks `Should I upload example data to Postgres (overwriting "feast_driver_hourly_stats" table)?`

