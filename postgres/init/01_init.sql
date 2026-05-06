-- Initialization script for the Data Warehouse
-- This runs automatically when the Postgres container is created for the first time.

-- Create schemas for different stages of the ETL pipeline
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS mart;

-- Grant usage on schemas to the main user (postgres in our case)
GRANT ALL ON SCHEMA raw TO postgres;
GRANT ALL ON SCHEMA mart TO postgres;
