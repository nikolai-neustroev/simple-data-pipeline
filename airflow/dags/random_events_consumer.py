import datetime

from airflow.decorators import dag, task

@dag(
        start_date=datetime.datetime(2024, 9, 28),
        catchup=False,
        schedule_interval=None,
        )
def random_events_consumer_dag():
    @task.virtualenv(
        requirements=["clickhouse-driver==0.2.9"],
        system_site_packages=False,
    )
    def init_db():
        from clickhouse_driver import Client

        clickhouse = Client(host='clickhouse', port=9000, user='default', password='')
        clickhouse.execute('''
        CREATE TABLE IF NOT EXISTS random_events (
            uuid String,
            value Float64,
            timestamp DateTime
        ) ENGINE = MergeTree()
        ORDER BY timestamp
        ''')

    @task.virtualenv(
        requirements=["kafka-python-ng==2.2.2", "numpy==2.1.1", "clickhouse-driver==0.2.9"],
        system_site_packages=False,
    )
    def consumer():
        import json
        from kafka import KafkaConsumer
        from clickhouse_driver import Client
        import logging

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        consumer = KafkaConsumer(
            'random_events',
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='clickhouse-consumer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        clickhouse = Client(host='clickhouse', port=9000, user='default', password='')
        for message in consumer:
            event = message.value
            event['timestamp'] = int(event['timestamp'] / 1000)  # Convert ms to seconds
            clickhouse.execute('INSERT INTO random_events (uuid, value, timestamp) VALUES', [(
                event['uuid'],
                event['value'],
                event['timestamp']
            )])
            logger.info(f"Inserted into ClickHouse: {event}")

    init_db_task = init_db()
    run_consumer = consumer()

    init_db_task >> run_consumer


random_events_consumer_dag()
