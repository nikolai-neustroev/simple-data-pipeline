import datetime

from airflow.decorators import dag, task

@dag(
        start_date=datetime.datetime(2024, 9, 28),
        catchup=False,
        schedule_interval=None,
        )
def random_events_producer_dag():
    @task.virtualenv(
        requirements=["kafka-python-ng==2.2.2", "numpy==2.1.1"],
        system_site_packages=False,
    )
    def producer():
        import uuid
        import json
        import time
        import numpy as np
        from kafka import KafkaProducer
        from kafka.errors import NoBrokersAvailable
        import logging
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        def create_producer(retries=5, delay=5):
            for attempt in range(retries):
                try:
                    producer = KafkaProducer(
                        bootstrap_servers='kafka:9092',
                        value_serializer=lambda v: json.dumps(v).encode('utf-8')
                    )
                    logger.info("Connected to Kafka successfully.")
                    return producer
                except NoBrokersAvailable:
                    logger.warning(f"Attempt {attempt + 1} of {retries}: Kafka brokers not available. Retrying in {delay} seconds...")
                    time.sleep(delay)
            logger.error("All attempts to connect to Kafka have failed.")
            raise NoBrokersAvailable("Could not connect to any Kafka brokers.")
        
        kafka_producer = create_producer()
        
        topic = 'random_events'
        
        try:
            while True:
                event = {
                    'uuid': str(uuid.uuid4()),
                    'value': float(np.random.normal()),
                    'timestamp': int(time.time() * 1000)
                }
                kafka_producer.send(topic, event)
                logger.info(f"Sent: {event}")
                time.sleep(30)  # Send an event every 30 seconds
        except KeyboardInterrupt:
            logger.info("Stopping producer.")
        finally:
            kafka_producer.close()
            logger.info("Producer closed.")

    run_producer = producer()
    run_producer


random_events_producer_dag()
