import os
import json
from kafka import KafkaConsumer
import logging
from services import LocationService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-consumer-service")

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_HOST = os.environ["KAFKA_HOST"]

# Create the kafka consumer
consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_HOST])

while True:
    for message in consumer:
        msg_json = message.value.decode()
        location = json.loads(msg_json)
        logger.info('Create location record', location)
        LocationService.create(location)
