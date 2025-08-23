import json
import unittest

import xmltodict

from weather_and_tide import (
    config,
    email_generator,
    mailer,
    response_parser
)


class TestSendEmail(unittest.TestCase):
    def setUp(self):
        with open(config.PACKAGE_ROOT / "tests/cached_api_responses/tide.json") as tr:
            self.tide_response = json.load(tr)
        with open(config.PACKAGE_ROOT / "tests/cached_api_responses/weather.xml") as wr:
            self.weather_response = xmltodict.parse(wr.read())

    def test_sanity(self):
        self.assertTrue(True)

    def test_generateThenSendEmail(self):
        tide_rows = response_parser.parse_forecast(self.tide_response)
        weather_rows = response_parser.parse_forecast(self.weather_response)
        email_data = {
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