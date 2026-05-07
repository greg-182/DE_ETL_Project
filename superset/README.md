# Data Visualization (Apache Superset)

This directory contains the configuration and build context for Apache Superset, our data visualization platform.

## Setup

Superset runs in its own set of Docker containers:
- `superset-init`: A one-time bootstrap container that runs database migrations and creates the initial admin user.
- `superset`: The main web server for the UI.

To prevent metadata conflicts, Superset uses its own internal Postgres database (`superset_meta`) and user (`superset`) within our shared Postgres container.

## Accessing the UI

Once the infrastructure is running (`make up`), you can access Superset at:

- **URL:** [http://localhost:8089](http://localhost:8089)
- **Username:** `admin`
- **Password:** `admin`

*(Note: We use port 8089 to avoid conflicts with Airflow and other local Superset instances.)*

## Connecting the Data Warehouse

To visualize our transformed Formula 1 data, you need to connect Superset to our `f1_warehouse` database:

1. Log into Superset.
2. Go to **Settings** (top right corner) -> **Database Connections**.
3. Click **+ Database** and select **PostgreSQL**.
4. Connect using the following SQLAlchemy URI:
   ```text
   postgresql+psycopg2://postgres:postgres@postgres:5432/f1_warehouse
   ```
5. Click **Connect** and finish the setup.

## Creating Dashboards

Once connected, you can add Datasets from the `mart` schema (e.g., `mart.f1_race_results`) and start building charts and dashboards!
