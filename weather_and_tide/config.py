from dataclasses import dataclass
import json
import os
from pathlib import Path

from dotenv import load_dotenv
import yaml

PACKAGE_ROOT = Path(__file__).parent
PROJECT_ROOT = PACKAGE_ROOT.parent

load_dotenv()
APIVERVE_API_KEY = os.getenv("APIVERVE_API_KEY") or "NO_KEY"
STORMGLASS_API_KEY = os.getenv("STORMGLASS_API_KEY") or "NO_KEY"
SEND_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS") or "NO_SENDER"
SEND_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD") or "NO_PASSWORD"

with open(PROJECT_ROOT / "county_to_fips.json") as cf:
    counties_to_fips: dict[str, str] = json.load(cf)

def _get_fips_from_county(names: list[str]) -> list[str]:
    return [counties_to_fips[name.lower()] for name in names]


@dataclass
class Location:
    name: str
    coords: tuple[float, float]
    info: str


@dataclass
class Config:
    email_recipients: list[str]
    county_warnings: list[str]
    locations: list[Location]


def load_config(config_file: Path) -> Config:
    """
    Load location data from a YAML file and return a Config object.

    Args:
        config_file (Path): The path to the YAML file containing location data.

    Returns:
        Config: An object with fields for the recipients of forecast emails, which counties
        to give weather warnings for, and the Locations (weather or tide) to forecast
    """
    with open(config_file) as lf:
        config = yaml.load(lf, Loader=yaml.Loader)
    email_recipients: list[str] = config["recipients"]
    county_warnings: list[str] = _get_fips_from_county(config["county_warnings"])
    location_objects: list[Location] = []
    for location in config["locations"]:
        coords = location["coords"].values()
        location_objects.append(Location(location["name"], coords, location["info"]))
    return Config(email_recipients, county_warnings, location_objects)
