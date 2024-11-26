import json
import unittest

import config
import email_generator
import response_parser

import xmltodict


class TestResponseParse(unittest.TestCase):
    def setUp(self):
        locations_file = config.PROJECT_ROOT + '/example.locations.yaml'
        self.locations = config.load_locations(locations_file)
        cache_files = config.PROJECT_ROOT + '/tests/cached_api_responses'
        moon_cache = cache_files + '/moon.json'
        with open(moon_cache) as mc:
            self.moon = json.load(mc)
        weather_cache = cache_files + '/weather.xml'
        with open(weather_cache, 'rb') as wc:
            self.weather = xmltodict.parse(wc)
        tide_cache = cache_files + '/tide.json'
        with open(tide_cache) as tc:
            self.tide = json.load(tc)

    def test_tideResponseToMail(self):
        moon_phase_fmt = response_parser.format_moon_phase(self.moon)
        fmt_rows = [response_parser.parse_forecast(forecast)
                    for forecast in (self.weather, self.tide)]

        email_data = { "moon_phase": moon_phase_fmt, 'locations': [] }
        for location, row_data in zip(self.locations, fmt_rows):
            location_summary = {
                'name': location.name,
                'type': location.info,
                'rows': row_data
            }
            email_data['locations'].append(location_summary)

        html_email = email_generator.generate_email(email_data)
        email_file = config.PROJECT_ROOT + '/tests/integration/generated_email.html'
        with open(email_file, 'w') as ef:
            ef.write(html_email)
