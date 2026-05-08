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
* `dbt/` - Data transformation models.
* `superset/` - Data visualization.

## Quick Start
Run these commands inside the VS Code Dev Container terminal:

1. **Initialize the Environment:**
   ```bash
   make init
   ```
   *Note: This creates a local Python virtual environment (`.venv`) and installs necessary dependencies for manual execution.*

2. **Start the Infrastructure:**
   ```bash
   make up
   ```
   *Note: This builds the custom images and starts Postgres, Airflow, and Superset. Services run on alternate ports (Postgres on 5433, Airflow UI on 8081, Superset on 8089) to prevent conflicts.*

3. **Access Airflow UI:**
   - Open your browser to <http://localhost:8081>
   - **Username:** `admin`
   - **Password:** `admin`
   - You can unpause and trigger the `f1_race_extraction_dag` from here to extract data and run dbt models.

4. **Access Superset UI:**
   - Open your browser to <http://localhost:8089>
   - **Username:** `admin`
   - **Password:** `admin`

5. **Run Manual Extraction (Optional):**
   If you don't want to use Airflow, you can run the extraction script manually:
   ```bash
   make etl-extract
   ```

6. **Verify the Data:**
   Open an interactive SQL shell to query the raw or transformed data:
   ```bash
   make db-shell
   ```
   *Example Query:* `SELECT * FROM mart.f1_race_results LIMIT 5;`

7. **Stop Everything:**
   ```bash
   make down
   ```
   *(Or `make reset-volumes` to wipe the databases clean)*

## Authors
Georg Allikas, Jüri Andrejev, Viktor Lantov 