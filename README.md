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
* **Dev Containers Extension** installed in VS Code.

## Project Structure
We follow a modular approach. Each directory contains its own `README.md` with specific instructions:
* `.devcontainer/` - Contains the environment definition for VS Code.
* `postgres/` - Scripts and configurations for our Data Warehouse. *(Pending)*
* `etl/` - Python scripts for extracting FastF1 data. *(Pending)*
* `airflow/` - DAGs and orchestration configuration. *(Pending)*
* `dbt/` - Data transformation models. *(Pending)*
* `superset/` - Dashboards and data visualization. *(Pending)*

## Quick Start
1. **Open the project in a Devcontainer:**
   * Open this folder in VS Code.
   * Press `F1` (or `Ctrl+Shift+P`), type `Dev Containers: Rebuild and Reopen in Container`, and hit Enter.
   * Wait for the container to build and the `post-create.sh` script to install Python dependencies.

2. **Start the Infrastructure:**
   Once inside the Devcontainer, open a terminal and run:
   ```bash
   docker-compose up -d
   ```
   *Note: Our services run on alternate ports (e.g., Postgres on 5433) to prevent conflicts with other projects.*
