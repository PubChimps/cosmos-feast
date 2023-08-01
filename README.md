# cosmos-feast

## Table of Contents
### Prereqs
### dbt
### Astronomer CLI

## Prereqs

## Snowflake
### Add parquet file
Download snowsql
`snowsql -a YOUR_SNOWFLAKE_ACCOUNT;`
```
USE ROLE YOUR_SNOWFLAKE_ROLE;
USE WAREHOUSE YOUR_SNOWFLAKE_WAREHOUSE;
USE DATABASE YOUR_SNOWFLAKE_DATABASE;
USE SCHEMA FEAST;
```
`PUT file://~/Downloads/credit_scores.parquet @PARQUET_TEST auto_compress=true;` 
`CREATE table if not exists PARQUET_VARIANT(src variant);`

```
COPY INTO PARQUET_VARIANT FROM (
    SELECT $1
        from @PARQUET_TEST/credit_scores.parquet
) file_format = (type=PARQUET COMPRESSION=SNAPPY); 
```
```
create table credit_scores as
    select src:__index_level_0__::integer as index,
        src:amount::double as amount,
        src:isFlaggedFraud::integer as isFlaggedFraud,
        src:isFraud::integer as isFraud,
        src:nameDest::varchar as nameDest,
        src:nameOrig::varchar as nameOrig,
        src:timestamp::TIMESTAMP_LTZ as timestamp,
        src:type_CASH_IN::INTEGER as type_CASH_IN,
        src:type_CASH_OUT,
        src:type_DEBIT,
        src:type_PAYMENT,
        src:type_TRANSFER)
    from parquet_variant;
```

```
create table credit_scores as select src:__index_level_0__:
                                    :integer as index,src:credit_score::integer as credit_score
                                    ,src:date::TIMESTAMP_NTZ as date,src:timestamp::TIMESTAMP_N
                                    TZ as timestamp,src:user_id::varchar as user_id from parque
                                    t_variant;
```
## dbt

## Astronomer CLI
The Astro CLI is a command line interface that makes it easy to get started with Apache Airflow, where will be orchestrating dbt and feast together in data pipelines called DAGs. Many other data and cloud services can be easily added to this example DAG, or run as separate DAGs, via the Astronomer Registry

### Install Astronomer CLI
```
brew install astro
mkdir astro && cd astro
astro dev init
```

### Add Cosmos to Astronomer
