from dataclasses import dataclass
from dotenv import load_dotenv
from collections import namedtuple
import os
from pathlib import Path
import yaml

load_dotenv()
STORMGLASS_API_KEY = os.getenv('STORMGLASS_API_KEY')

Coords = namedtuple('Coords', ('lat', 'long'))

@dataclass
class Location:
    name: str
    coords: Coords
    info: str

def load_locations(locations_file: Path) -> tuple[Location, ...]:
    with open(locations_file) as lf:
        raw_locations = yaml.load(lf, Loader=yaml.Loader)
    location_objects: list[Location] = []
    for location in raw_locations:
        coords = Coords(*location['coords'].values())
        location_objects.append(Location(location['name'], coords, location['info']))
    return tuple(location_objects)