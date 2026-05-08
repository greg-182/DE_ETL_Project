# Data Warehouse (Postgres)

This directory contains the initialization scripts and configuration for our Postgres Data Warehouse. 

## Schemas
When the database is first initialized, it creates two primary schemas:
1. **`raw`**: This schema acts as our Data Lake / Staging area. The Python ETL scripts will extract data from the FastF1 API and dump it directly here with minimal transformation.
2. **`mart`**: This schema acts as our Data Mart. `dbt` (Data Build Tool) will read from the `raw` schema, clean the data, apply business logic, and save the final dimensional models (facts and dimensions) into this schema. Superset will connect to `mart` to build visualizations.

## Connection Details
You can connect to this database using a database client like **DBeaver** or **DataGrip** from your host machine.

Use the following credentials (defined in the root `.env` file):
* **Host**: `localhost` (or `127.0.0.1`)
* **Port**: `5433` (We use 5433 to avoid conflicts with other local projects)
* **Database**: `f1_warehouse`
* **Username**: `postgres`
* **Password**: `postgres`

## How to interact via Terminal
If you are inside the Dev Container and want to quickly query the database via the command line, run our Makefile shortcut:
```bash
make db-shell
```

Alternatively, you can run the raw docker exec command:
```bash
sudo docker exec -it f1_etl_project-postgres-1 psql -U postgres -d f1_warehouse
```

To list the schemas:
```sql
\dn
```
To exit `psql`:
```sql
\q
```
