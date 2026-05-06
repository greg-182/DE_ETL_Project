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
* **Port**: `5433` (We use 5433 to avoid conflicting with the teacher's default 5432 port)
* **Database**: `f1_warehouse`
* **Username**: `postgres`
* **Password**: `postgres`

## How to interact via Terminal
If you are inside the Dev Container and want to quickly query the database via the command line, run:
```bash
PGPASSWORD=postgres psql -h postgres -U postgres -d f1_warehouse -p 5432
```
*(Note: Inside the docker network, the hostname is `postgres` and the internal port is `5432`. The `5433` port is only for connections from outside the Docker network, like your host machine).*

To list the schemas:
```sql
\dn
```
To exit `psql`:
```sql
\q
```
