import json
import unittest

import config
import email_generator
import response_parser

import xmltodict


class TestResponseParse(unittest.TestCase):
    def setUp(self):
        locations_file = config.PROJECT_ROOT + '/locations.yaml.example'
        self.locations = config.load_locations(locations_file)
        cache_files = config.PROJECT_ROOT + '/tests/cached_api_responses'
        weather_cache = cache_files + '/weather.xml'
        with open(weather_cache, 'rb') as wc:
            self.weather: dict = xmltodict.parse(wc)
        tide_cache = cache_files + '/tide.json'
        with open(tide_cache) as tc:
            self.tide: dict = json.load(tc)

    def test_tideResponseToMail(self):
        fmt_rows = [response_parser.parse_forecast(forecast)
                    for forecast in (self.weather, self.tide)]

        email_data = { 'locations': [] }
        for location, row_data in zip(self.locations, fmt_rows):
            location_summary = {
                'name': location.name,
                'type': location.info,
                'rows': row_data
            }
            email_data['locations'].append(location_summary)

        html_email: str = email_generator.generate_email(email_data)
        email_file = config.PROJECT_ROOT + '/tests/integration/generated_email.html'
        with open(email_file, 'w') as ef:
            ef.write(html_email)
