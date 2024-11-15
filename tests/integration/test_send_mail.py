import email_generator
import json
import mailer
import response_parser
import unittest
import xmltodict


class TestSendEmail(unittest.TestCase):
    def test_sanity(self):
        self.assertTrue(True)

    def test_generateThenSendEmail(self):
        with open('../cached_api_responses/tide.json') as tr:
            tide_response = json.load(tr)
        with open('../cached_api_responses/weather.xml', 'rb') as wr:
            weather_response = xmltodict.parse(wr)
        tide_rows = response_parser._generate_tide_rows(tide_response)
        weather_rows = response_parser._generate_weather_rows(weather_response)
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
            ]
        }
        html_email = email_generator.generate_email(email_data)
        mailer.send_email(html_email, "today!")