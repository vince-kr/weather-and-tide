from dataclasses import dataclass
from dotenv import load_dotenv
import os
from pathlib import Path
import yaml

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

load_dotenv()
APIVERVE_API_KEY = os.getenv('APIVERVE_API_KEY') or "NO_KEY"
STORMGLASS_API_KEY = os.getenv('STORMGLASS_API_KEY') or "NO_KEY"
SEND_EMAIL_ADDRESS = os.getenv('SENDER_EMAIL_ADDRESS') or "NO_SENDER"
SEND_EMAIL_PASSWORD = os.getenv('SENDER_EMAIL_PASSWORD') or "NO_PASSWORD"

@dataclass
class Location:
    name: str
    coords: tuple[float, float]
    info: str

@dataclass
class Config:
    email_recipients: list[str]
    locations: list[Location]

def load_config(config_file: Path) -> Config:
    """
    Load location data from a YAML file and return it as a tuple of Location objects.

    Args:
        config_file (Path): The path to the YAML file containing location data.

    Returns:
        tuple[Location, ...]: A tuple of Location objects, each representing a location
        with a name, coordinates, and the type of information to fetch.
    """
    with open(config_file) as lf:
        config = yaml.load(lf, Loader=yaml.Loader)
    email_recipients: list[str] = config['recipients']
    location_objects: list[Location] = []
    for location in config['locations']:
        coords = location['coords'].values()
        location_objects.append(Location(location['name'], coords, location['info']))
    return Config(email_recipients, location_objects)