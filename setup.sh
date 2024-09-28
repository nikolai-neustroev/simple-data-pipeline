#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Create the Airflow database
echo "Creating Airflow database..."
docker-compose exec postgres-airflow psql -U postgres -c "CREATE DATABASE airflow;"

# Initialize the Redash database
echo "Initializing Redash database..."
docker-compose run --rm redash create_db

echo "Database setup completed successfully."
