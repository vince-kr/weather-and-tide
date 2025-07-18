import json
import unittest
import xmltodict

import config
import email_generator
import mailer
import response_parser


class TestSendEmail(unittest.TestCase):
    def setUp(self):
        with open(config.PROJECT_ROOT / "tests/cached_api_responses/moon.json") as mr:
            self.moon_response = json.load(mr)
        with open(config.PROJECT_ROOT / "tests/cached_api_responses/tide.json") as tr:
            self.tide_response = json.load(tr)
        with open(config.PROJECT_ROOT / "tests/cached_api_responses/weather.xml") as wr:
            self.weather_response = xmltodict.parse(wr.read())

    def test_sanity(self):
        self.assertTrue(True)

    def test_generateThenSendEmail(self):
        moon_phase = response_parser.format_moon_phase(self.moon_response)
        tide_rows = response_parser._generate_tide_rows(self.tide_response)
        weather_rows = response_parser._generate_weather_rows(self.weather_response)
        email_data = {
            'moon_phase': moon_phase,
            'locations': [
                {
                    "name": "Bray Head",
                    "type": "weather",
                    "rows": weather_rows
                },
                {
                    'name': 'Bray Seafront',
                    'type': 'tide',
                    'rows': tide_rows
                }
            ],
            'recipients': []
        }
        html_email = email_generator.generate_email(email_data)
        mailer.send_email(html_email, email_data['recipients'], "today!")