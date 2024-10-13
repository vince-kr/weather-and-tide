import config_loader
import unittest
from pathlib import Path

class TestLoadingLocations(unittest.TestCase):
    def setUp(self):
        self.valid_locations = Path('test-locations_valid.yaml')
        self.invalid_locations = Path('test-locations_invalid.yaml')

    def test_sanity(self):
        self.assertTrue(1)

    def test_whenLocationsLoaded_thenAccessLocationAttributes(self):
        locations = config_loader.load_locations(self.valid_locations)
        print(locations)
        first_location = locations[0]
        expected = 'Bray Head', (53.1909, -6.0839), 'weather'
        actual = first_location.name, first_location.coords, first_location.info
        self.assertEqual(expected, actual)