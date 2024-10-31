import datetime

import api_caller
import unittest

class TestApiCaller(unittest.TestCase):
    def setUp(self):
        date_today = datetime.date.today()
        self.start_of_today = date_today.isoformat() + 'T00:00:00'
        date_tomorrow = date_today + datetime.timedelta(days=1)
        self.start_of_tomorrow = date_tomorrow.isoformat() + 'T00:00:00'

    def test_sanity(self):
        self.assertTrue(True)

    def test_generateWeatherRequestObject(self):
        coords = (53.2048, -6.0979)
        base_url = 'http://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast'
        expected = {
            'url': base_url + f'?lat=53.2048;long=-6.0979'
        }
        actual = api_caller._build_weather_request(coords)
        self.assertEqual(expected, actual)

    def test_generateTideRequestObject(self):
        base_url = 'https://api.stormglass.io/v2/tide/extremes/point'
        lat, long = (53.2048, -6.0979)
        api_key = 'not-really-an-api-key'
        expected = {
            'url': base_url,
            'params': {
                'lat': lat,
                'lng': long,
                'start': self.start_of_today,
                'end': self.start_of_tomorrow
            },
            'headers': {
                'Authorization': api_key
            }
        }
        actual = api_caller._build_tide_request((lat, long), api_key)
        self.assertEqual(expected, actual)
