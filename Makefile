.PHONY: help init up down etl-extract

# Default target when just running 'make'
.DEFAULT_GOAL := help

help:
	@echo "Targets:"
	@echo "  make init           Create .venv and install Python dependencies"
	@echo "  make up             Start the infrastructure (Postgres, etc.) in the background"
	@echo "  make down           Stop and remove the infrastructure containers"
	@echo "  make etl-extract    Run the Python script to extract FastF1 data into Postgres"
	@echo "  make db-shell       Open an interactive SQL shell to view the data"

# Create local virtual environment in the devcontainer (idempotent)
init:
	@.venv/bin/python --version >/dev/null 2>&1 || (echo "Setting up python environment..." && bash .devcontainer/post-create.sh)

# Start the infrastructure
up:
	sudo -E docker compose up -d --build
	@echo "Attaching Dev Container to the project network..."
	@sudo docker network connect f1_etl_project_default $$(hostname) 2>/dev/null || true

# Stop the infrastructure
down:
	sudo -E docker compose down

# Stop the infrastructure and wipe all data volumes
reset-volumes:
	sudo -E docker compose down -v

# Run the Python extraction script
etl-extract: init
	.venv/bin/python etl/extract_race_results.py

# Open interactive Postgres shell
db-shell:
	sudo docker exec -it f1_etl_project-postgres-1 psql -U postgres -d f1_warehouse
