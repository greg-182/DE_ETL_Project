# Data Transformation (dbt)

This directory contains our dbt (Data Build Tool) project, which is responsible for the **Transform** phase of our ETL pipeline.

## Structure

- `dbt_project.yml`: The main configuration file for the dbt project.
- `profiles.yml`: Connection settings for our Postgres Data Warehouse.
- `models/staging/`: Views that read directly from the `raw` schema, clean up column names, and cast types (e.g., `stg_race_results.sql`).
- `models/marts/`: Final materialized tables that apply business logic and filtering, ready for visualization (e.g., `f1_race_results.sql`).
- `macros/`: Custom SQL macros, such as overriding the default schema naming convention.

## How it runs

Normally, dbt is automatically triggered by Airflow immediately after the FastF1 extraction task completes. The Airflow DAG mounts this directory and executes the models inside the Airflow container's Python environment.

## Manual Execution

If you need to run or test dbt manually, you can execute it from inside the Airflow scheduler container using our project configuration:

```bash
docker exec -it f1_etl_project-airflow-scheduler-1 dbt run --project-dir /opt/airflow/dbt --profiles-dir /opt/airflow/dbt
```
