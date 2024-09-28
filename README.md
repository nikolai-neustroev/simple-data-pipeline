# simple-data-pipeline
A simple data warehouse pipeline that generates events, streams them through Kafka, stores them in ClickHouse, visualizes them with Redash, and orchestrates the workflow with Airflow.

# Overview

The Simple Data Pipeline project showcases a basic yet effective data ingestion and storage system. It leverages:

1. Apache Airflow for orchestrating data workflows.
2. Kafka as the message broker for real-time data streaming.
3. ClickHouse as a high-performance columnar database for storing and querying large volumes of data.
4. Redash for data visualization.

# Prerequisites

Before setting up the project, ensure you have the following installed:

1. Docker Desktop
2. Python >3.9

# Installation

Follow these steps to set up and run the Simple Data Pipeline project locally.

## Clone the Repository

```
git clone https://github.com/your-username/simple-data-pipeline.git
cd simple-data-pipeline
```

## Install Dependencies

Ensure you have Python installed. It's recommended to use a virtual environment.

```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Start Services with Docker Compose

Launch all necessary services using Docker Compose.

```
docker-compose up -d
```

## Initialize Databases

Run the setup script to initialize the Airflow and Redash databases.

```
sh setup.sh
```

## Access Airflow UI

Once the services are up and running, access the Airflow web interface to manage DAGs.

Airflow UI: http://localhost:8080
Default credentials (if not set otherwise):
```
Username: admin
Password: admin
```

Activate and run random_events_producer_dag and then random_events_consumer_dag. The first DAG runs a Kafka producer generating random values and the second DAG stores events in Clickhouse.

## Access Redash

Access Redash to work with data visualization.

Redash: http://localhost:5001

Follow the setup instructions to create an admin account.

Add ClickHouse as a Data Source:

Navigate to: Settings > Data Sources > + New Data Source.

Select: ClickHouse

Configure:

Name: ClickHouse

Host: http://clickhouse:8123

Database: default (or your specific database)

User: (if set)

Password: (if set)

Test & Save.

Create a Query and Visualization:

Navigate to: Queries > New Query.

Select: ClickHouse as the data source.

Write a Query:
```
SELECT
    toDateTime(timestamp) AS event_time,
    value
FROM random_events
ORDER BY event_time DESC
LIMIT 1000
```

Visualize: Choose a visualization type, such as a line chart, to plot value over event_time.

Save the query and add it to a dashboard.
