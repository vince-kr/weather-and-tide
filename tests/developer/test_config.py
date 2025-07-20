from pathlib import Path

import pytest

import config

@pytest.fixture
def valid_locations():
    return Path(config.PROJECT_ROOT / "tests/test-locations_valid.yaml")

def test_when_locations_loaded_then_access_location_attributes(valid_locations):
    locations = config.load_config(valid_locations).locations
    first_location = locations[0]
    expected = "Bray Head", (53.1909, -6.0839), "weather"
    actual = first_location.name, tuple(first_location.coords), first_location.info
    assert expected == actual
