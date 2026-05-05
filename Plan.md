# FastF1 ETL Pipeline Plan

This document outlines the step-by-step implementation plan for the F1 Data Engineering project. Following best practices, every directory will contain a local `README.md` explaining its contents, prerequisite steps, and terminal commands to run the code.

## Postgres vs DuckDB: A Quick Primer
*   **Postgres:** A traditional, robust, "always-on" database server. It handles concurrent connections very well and is the standard for transactional systems.
*   **DuckDB:** A fast, serverless, in-process analytical database (like SQLite, but designed for OLAP/data analysis). It doesn't require a background server to run and is incredibly fast for reading large datasets.
*   **Our Choice:** We will use **Postgres** (with potentially a DuckDB extension for analytics if we follow the teacher's image `pgduckdb/pgduckdb`), acting as our main Data Warehouse for structured storage and connection to Superset.

---

## Phase 1: Foundation (Environment & Global Docs)
*   [ ] Set up `.devcontainer` configuration to ensure reproducible environments.
*   [ ] Set up `docker-compose.yml` and `.env` for managing our isolated project services.
*   [ ] Create a global `README.md` containing overall project structure, prerequisites, and startup instructions.

## Phase 2: Data Warehouse (Postgres)
*   [ ] Configure Postgres database in `docker-compose.yml`.
*   [ ] Create `postgres/` directory with initialization scripts for `raw` and `mart` schemas.
*   [ ] Write a `postgres/README.md` documenting the schema design and commands to connect to the database via terminal/DBeaver.

## Phase 3: Data Extraction (Python -> FastF1 API)
*   [ ] Create an `etl/` directory for Python extraction scripts.
*   [ ] Write a Python script to fetch F1 data (e.g., race results, telemetry) from FastF1 API.
*   [ ] Load the fetched data into the Postgres `raw` schema.
*   [ ] Write `etl/README.md` detailing the API endpoints used and the exact terminal commands to run the extraction scripts manually.

## Phase 4: Orchestration (Airflow)
*   [ ] Configure Airflow services in `docker-compose.yml`.
*   [ ] Create `airflow/dags/` directory and configure Airflow connections.
*   [ ] Write a DAG to schedule the Python extraction scripts to run automatically.
*   [ ] Write `airflow/README.md` explaining how to access the Airflow UI, trigger DAGs, and check logs.

## Phase 5: Transformation (dbt)
*   [ ] Create a `dbt/` directory and initialize a dbt project.
*   [ ] Write SQL models to transform the data from the `raw` schema into a clean, dimensional structure in the `mart` schema.
*   [ ] Set up testing and documentation within dbt.
*   [ ] Write `dbt/README.md` explaining how to run `dbt run`, `dbt test`, and generate dbt docs.

## Phase 6: Visualization (Superset)
*   [ ] Configure Superset in `docker-compose.yml`.
*   [ ] Connect Superset to the Postgres `mart` schema.
*   [ ] Build a dashboard to visualize F1 insights.
*   [ ] Write `superset/README.md` detailing how to log in, configure the database connection, and import/export dashboards.

## Phase 7: Final Polish & Report
*   [ ] Ensure all local `README.md` files are up-to-date and accurate.
*   [ ] Write the 500-700 word project report required by the assignment inside a `report.md` file.
*   [ ] Verify the GitHub repository is clean, documented, and ready for submission.