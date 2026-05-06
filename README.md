# FastF1 ETL Pipeline Project

This project implements an end-to-end Data Engineering ETL (Extract, Transform, Load) pipeline. It extracts Formula 1 data from the [FastF1 API](https://docs.fastf1.dev/), loads it into a Postgres Data Warehouse, transforms it using dbt, orchestrates the workflow using Airflow, and visualizes the results with Apache Superset.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)

## Prerequisites
To run this project smoothly without conflicting with other local setups, we use a Devcontainer.
* **Docker Desktop** installed and running.
* **Visual Studio Code (VS Code)** installed.
* **Dev Containers Extension** installed.

## Project Structure
We follow a modular approach. Each directory contains its own `README.md` with specific instructions:
* `.devcontainer/` - Contains the environment definition.
* `postgres/` - Scripts and configurations for our Data Warehouse.
* `etl/` - Python scripts for extracting FastF1 data.
* `airflow/` - DAGs and orchestration configuration.
* `dbt/` - Data transformation models. *(Pending)*
* `superset/` - Data visualization. *(Pending)*

## Quick Start
Run these commands inside the VS Code Dev Container terminal:

1. **Start the Infrastructure:**
   ```bash
   make up
   ```
   *Note: This builds the Airflow image and starts Postgres. Services run on alternate ports (e.g., Postgres on 5433, Airflow UI on 8081) to prevent conflicts with other projects.*

2. **Access Airflow UI:**
   - Open your browser to <http://localhost:8081>
   - **Username:** `admin`
   - **Password:** `admin`
   - You can unpause and trigger the `f1_race_extraction_dag` from here.

3. **Run Manual Extraction (Optional):**
   If you don't want to use Airflow, you can run the extraction script manually:
   ```bash
   make etl-extract
   ```

4. **Verify the Data:**
   Open an interactive SQL shell to query the raw data:
   ```bash
   make db-shell
   ```
   *Example Query:* `SELECT * FROM raw.race_results LIMIT 5;`

5. **Stop Everything:**
   ```bash
   make down
   ```
   *(Or `make reset-volumes` to wipe the database clean)*
