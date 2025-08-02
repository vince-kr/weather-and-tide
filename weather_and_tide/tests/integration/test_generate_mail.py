import json
import unittest

import xmltodict

from weather_and_tide import (
    config,
    email_generator,
    response_parser
)


class TestResponseParse(unittest.TestCase):
    def setUp(self):
        config_file = config.PROJECT_ROOT / "example.config.yaml"
        self.user_config = config.load_config(config_file)
        self.desired_counties = self.user_config.county_warnings
        cache_files = config.PACKAGE_ROOT / "tests/cached_api_responses"
        with open(cache_files / "warnings.json") as wc:
            self.warnings = json.load(wc)
        with open(cache_files / "moon.json") as mc:
            self.moon = json.load(mc)
        with open(cache_files / "weather.xml", "rb") as wc:
            self.weather = xmltodict.parse(wc)
        with open(cache_files / "tide.json") as tc:
            self.tide = json.load(tc)

    def test_generateFullEmail(self):
        warnings = response_parser.parse_warnings(self.warnings)
        moon_phase_fmt = response_parser.format_moon_phase(self.moon)
        fmt_rows = [
            response_parser.parse_forecast(forecast)
            for forecast in (self.weather, self.tide)
        ]

        email_data = {
            "warnings": warnings,
            "moon_phase": moon_phase_fmt,
            "locations": [],
        }
        for location, row_data in zip(self.user_config.locations, fmt_rows):
            location_summary = {
                "name": location.name,
                "type": location.info,
                "rows": row_data,
            }
            email_data["locations"].append(location_summary)

        html_email = email_generator.generate_email(email_data)
        email_file = config.PACKAGE_ROOT / "tests/integration/generated_email.html"
        with open(email_file, "w") as ef:
            ef.write(html_email)
