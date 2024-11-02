import xmltodict

import api_caller
import dotenv
import os
import requests
import unittest

dotenv.load_dotenv()

class TestApiResponses(unittest.TestCase):
    def setUp(self):
        self.coords = (53.2048, -6.0979)
        self.api_key = os.getenv('STORMGLASS_API_KEY')

    def test_sanity(self):
        self.assertTrue(True)

    def test_callTideApi_confirmContents(self):
        request_object = api_caller._build_tide_request(self.coords, self.api_key)
        response = requests.get(**request_object)
        self.assertTrue(response.ok)
        body: dict = response.json()
        self.assertTrue('data' in body)
        self.assertTrue(len(body['data']) > 0)

    def test_callWeatherApi_confirmContents(self):
        request_object = api_caller._build_weather_request(self.coords)
        response = requests.get(**request_object)
        self.assertTrue(response.ok)
        body: dict = xmltodict.parse(response.content)
        self.assertTrue('weatherdata' in body)
        self.assertTrue(len(body['weatherdata']) > 0)