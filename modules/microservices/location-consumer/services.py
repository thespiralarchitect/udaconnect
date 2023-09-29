import logging
from typing import Dict

from models import Location
from schemas import LocationSchema
from geoalchemy2.functions import ST_Point
import os 
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-api")

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

connect_url = engine.url.URL.create(
    'postgresql+psycopg2',
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
    port=DB_PORT
)
engine = create_engine(connect_url)
Session = sessionmaker(bind=engine)

class LocationService:
    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        session = Session()

        session.add(new_location)
        session.commit()

        return new_location
