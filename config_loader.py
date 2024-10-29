from dataclasses import dataclass
from dotenv import load_dotenv
import os
from pathlib import Path
import yaml

load_dotenv()
STORMGLASS_API_KEY = os.getenv('STORMGLASS_API_KEY')
SEND_EMAIL_ADDRESS = os.getenv('SENDER_EMAIL_ADDRESS')
SEND_EMAIL_PASSWORD = os.getenv('SENDER_EMAIL_PASSWORD')

@dataclass
class Location:
    name: str
    coords: tuple[float, float]
    info: str

def load_locations(locations_file: Path) -> tuple[Location, ...]:
    with open(locations_file) as lf:
        raw_locations = yaml.load(lf, Loader=yaml.Loader)
    location_objects: list[Location] = []
    for location in raw_locations:
        coords = tuple(location['coords'].values())
        location_objects.append(Location(location['name'], coords, location['info']))
    return tuple(location_objects)