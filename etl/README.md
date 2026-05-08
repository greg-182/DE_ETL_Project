# Data Extraction (ETL)

This directory contains the Python scripts responsible for the **Extract** and **Load** phases of our ETL pipeline.

We are using the `fastf1` Python library to communicate with the Formula 1 API.

## Scripts
*   `extract_race_results.py`: Connects to the FastF1 API, downloads the race results for a specific event (e.g., 2023 Bahrain Grand Prix or 2026 season), and loads it into the `raw.race_results` table in our Postgres Data Warehouse.

## How it works
1.  **Extract**: The script hits the FastF1 API endpoints and downloads race session data. FastF1 caches this data locally in the `etl/cache/` folder so we don't spam their API on repeated runs.
2.  **Transform**: Very minimal. We only filter down to the columns we need (Driver, Team, Position, Points, Laps) and add a `year` and `race_name` identifier. Heavy transformation is saved for dbt later.
3.  **Load**: Uses Pandas and SQLAlchemy to write the DataFrame directly to the `raw` schema in Postgres.

## How to run manually
While Airflow is typically used to automate this process, you can run the script manually from the Dev Container terminal using the Makefile at the root of the project:

```bash
make etl-extract
```
*(Ensure Postgres is running first by running `make up`!)*
