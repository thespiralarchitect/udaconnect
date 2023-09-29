import time
from concurrent import futures
from kafka import KafkaProducer

import json
import os
import grpc
import location_pb2
import location_pb2_grpc
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-producer-service")

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_HOST = os.environ["KAFKA_HOST"]

producer = KafkaProducer(bootstrap_servers=[KAFKA_HOST])

class LocationServer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        msg = {
            'person_id': int(request.person_id),
            'latitude': str(request.latitude),
            'longitude': str(request.longitude)
        }
        msg_json = json.dumps(msg)
        logger.info('Sending message to Kafka', {
            "message": msg_json,
            "topic": KAFKA_TOPIC,
            "host": KAFKA_HOST
        })

        producer.send('location_event', msg_json.encode())
        producer.flush()
        return location_pb2.LocationMessage(**msg)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServer(), server)

logger.info("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()
