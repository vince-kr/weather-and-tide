"""Create a module to convert API responses into useful objects"""
import json
import response_parser
import unittest


class TestTide(unittest.TestCase):
    def setUp(self):
        self.datetimestamp = "2024-09-26T18:31:00+00:00"
        with open("cached_api_responses/tide.json") as tf:
            self.response: dict = json.load(tf)

    def test_sanity(self):
        self.assertTrue(True)

    def test_givenBigDateTimeString_extractOnlyTime(self):
        expected = "18:31"
        actual = response_parser._extract_time_from(self.datetimestamp)
        self.assertEqual(expected, actual)

    def test_givenResponseAsDict_returnIterableOfTuples(self):
        expected = (
            (
                "Low",
                ("18:31",),
            ),
            (
                "High",
                ("00:49",),
            ),
            (
                "Low",
                ("07:07",),
            ),
        )
        actual = response_parser.format_tide_response(self.response)
        self.assertEqual(expected, actual)
