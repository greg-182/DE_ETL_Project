# Formula 1 Data Engineering ETL Project Report

## Objectives
The primary objective of this project was to design and implement a robust, end-to-end Data Engineering pipeline capable of extracting, transforming, and visualizing Formula 1 race data. Focused on the 2026 season, the pipeline aims to provide automated, actionable insights into driver standings, constructor performance, race lap times, overtaking statistics, and weather impacts. The project serves as a comprehensive demonstration of modern data engineering workflows, utilizing containerized environments and industry-standard orchestration and transformation tools.

## Data Sources
The sole data source for this project is the **FastF1 API**, an open-source Python library that provides access to F1 historical data, including lap timing, car telemetry, position, weather data, and session results. For this pipeline, we focused on race session data, extracting grid positions, final classifications, driver and team information, best and average lap times, and boolean indicators for wet/dry race conditions.

## ETL Process and Architecture
The project architecture is entirely containerized using Docker and VS Code Dev Containers, ensuring reproducibility and avoiding local dependency conflicts. The pipeline follows a classic Extract, Load, Transform (ELT) pattern:

1. **Extraction (Python & Pandas):** 
   A custom Python script (`extract_race_results.py`) connects to the FastF1 API. It loops through the official race schedule, downloading session results, lap data, and weather metrics. The data is parsed, merged, and cleaned into a structured Pandas DataFrame. To optimize performance and reduce API load, a local cache was implemented.
   
2. **Load (PostgreSQL):** 
   The structured DataFrame is loaded directly into a PostgreSQL Data Warehouse container using `SQLAlchemy`. The data lands in the `raw` schema (`raw.race_results`), acting as our immutable single source of truth for the pipeline.

3. **Transformation (dbt - Data Build Tool):** 
   Once the raw data is loaded, dbt takes over to model the data for analytical purposes. 
   - **Staging Models:** Clean up column names and explicitly cast data types (e.g., casting points and positions to numeric types).
   - **Mart Models:** Apply general logic to create presentation-ready tables. This includes `f1_race_results` (calculating positions gained and DNF flags), `f1_driver_standings` (using window functions for cumulative season points), and `f1_constructor_standings` (aggregating points by team).

4. **Orchestration (Apache Airflow):** 
   The entire workflow is automated via Apache Airflow. A Directed Acyclic Graph (DAG) scheduled to run weekly triggers the Python extraction script first, followed immediately by the `dbt run` command to update the analytical models.

## Visualization
For data consumption, **Apache Superset** was deployed alongside the database. Superset connects directly to the `mart` schema in PostgreSQL. We constructed an interactive dashboard featuring:
- Line charts tracking the evolution of Driver and Constructor championship standings.
- Bar charts highlighting the best overtakers (positions gained) and fastest lap times.
- Pie charts summarizing total driver retirements (DNFs) and the ratio of wet to dry races.

## Challenges Encountered and Addressed
1. **Port and Network Conflicts:** Running Postgres, Airflow, and Superset simultaneously often leads to port collisions with host machine services. 
   *Solution:* We configured Docker Compose to expose services on alternate ports (e.g., Postgres on 5433, Airflow on 8081, Superset on 8089) and utilized an isolated internal Docker network.

2. **Database View Dependencies during Reloads:** During the Load phase, pandas' default `if_exists='replace'` behavior dropped the `raw.race_results` table entirely. This caused `psycopg2.errors.DependentObjectsStillExist` errors because the dbt views depended on this table.
   *Solution:* The extraction script was modified to use a raw SQL `DROP TABLE ... CASCADE` command before appending new data. This safely cleared the table and dropped stale dependent views, which were then cleanly recreated by dbt in the subsequent pipeline step.

3. **API Rate Limiting and Payload Size:** Fetching lap-by-lap telemetry for an entire season is extremely slow and prone to timeouts.
   *Solution:* Telemetry data was explicitly disabled during the FastF1 session load (`telemetry=False`). Furthermore, a persistent cache directory was mapped to the Airflow container to store API responses, drastically reducing subsequent pipeline execution times.