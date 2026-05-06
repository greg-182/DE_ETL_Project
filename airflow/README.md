# Airflow Orchestration

This directory contains the configurations and DAGs (Directed Acyclic Graphs) for Apache Airflow, which orchestrates our FastF1 ETL pipeline.

## Setup
We run Airflow locally using Docker Compose, leveraging the official Airflow Docker images customized for our project.

The Airflow services running include:
- `airflow-scheduler`: Monitors DAGs and triggers tasks based on their schedules.
- `airflow-apiserver`: The web UI and API server for Airflow.
- `airflow-dag-processor`: Parses the Python files in the `dags/` folder to discover DAGs.
- `airflow-triggerer`: Handles deferred tasks (if any).

## Accessing the UI
Once the infrastructure is running via `make up`, you can access the Airflow Web UI from your host machine:

- **URL:** [http://localhost:8081](http://localhost:8081)
- **Username:** `admin`
- **Password:** `admin`

*(Note: We use port `8081` to avoid conflicts with other local Airflow instances.)*

## DAGs
All Airflow pipelines are defined in the `dags/` folder.

### `f1_race_extraction_dag`
- **Schedule:** Every Monday at 12:00 PM (`0 12 * * 1`)
- **Purpose:** Triggers the Python extraction script (`etl/extract_race_results.py`) to pull the latest Formula 1 data from the FastF1 API and load it into the Postgres Data Warehouse.
- **Execution:** It uses the `BashOperator` to execute the script securely within the Airflow container's Python virtual environment.

## Troubleshooting
If you don't see your DAGs in the UI, check the processor logs:
```bash
docker logs f1_etl_project-airflow-dag-processor-1
```
