import arrow
import dotenv
import os
import requests
import unittest

dotenv.load_dotenv()

class TestApiResponses(unittest.TestCase):
    def setUp(self):
        api_key = os.getenv('STORMGLASS_API_KEY')
        start = arrow.now().floor('day')
        end = arrow.now().shift(days=1).floor('day')
        self.request_object = {
            'url': 'https://api.stormglass.io/v2/tide/extremes/point',
            'params': {
                'lat': 53.2048,
                'lng': -6.0979,
                'start': start,
                'end': end
            },
            'headers': {
                'Authorization': api_key
            }
        }

    def test_sanity(self):
        self.assertTrue(True)  # add assertion here

    def test_callTideApi_confirmContents(self):
        response = requests.get(**self.request_object)
        self.assertTrue(response.ok)
        body: dict = response.json()
        self.assertTrue('data' in body)
        self.assertTrue(len(body['data']) > 0)