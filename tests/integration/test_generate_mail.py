import json
import unittest

import config
import email_generator
import response_parser

import xmltodict


class TestResponseParse(unittest.TestCase):
    def setUp(self):
        config_file = config.PROJECT_ROOT / "example.config.yaml"
        self.user_config = config.load_config(config_file)
        cache_files = config.PROJECT_ROOT / "tests/cached_api_responses"
        with open(cache_files / "warnings.json") as wc:
            self.warnings = json.load(wc)
        with open(config.PROJECT_ROOT / "county_to_fips.json") as ff:
            self.counties_to_fips = json.load(ff)
        with open(cache_files / "moon.json") as mc:
            self.moon = json.load(mc)
        with open(cache_files / "weather.xml", "rb") as wc:
            self.weather = xmltodict.parse(wc)
        with open(cache_files / "tide.json") as tc:
            self.tide = json.load(tc)

    def test_generateFullEmail(self):
        warnings = response_parser.format_warnings(
            self.warnings, self.user_config.county_warnings, self.counties_to_fips
        )
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
        email_file = config.PROJECT_ROOT / "tests/integration/generated_email.html"
        with open(email_file, "w") as ef:
            ef.write(html_email)
