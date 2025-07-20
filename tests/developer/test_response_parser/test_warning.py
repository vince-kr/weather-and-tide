import json
import unittest

import config
import response_parser


class TestWarning(unittest.TestCase):
    def setUp(self):
        with open(
                config.PROJECT_ROOT / "tests/cached_api_responses/warnings.json"
        ) as wf:
            self.response: list[dict] = json.load(wf)
        with open(config.PROJECT_ROOT / "county_to_fips.json") as cf:
            self.COUNTIES_TO_FIPS: dict[str, str] = json.load(cf)
        self.desired_counties = ["Dublin", "Wicklow"]

        response_template = dict(
            id=0,
            level="Yellow",
            headline="Scary weather warning!",
            onset="2024-09-26T18:31:00+00:00",
            expiry="2024-09-27T18:31:00+00:00",
            description="Batten down the hatches.",
            regions=["EI02"]
        )

        self.yellow = dict(response_template)
        self.yellow["id"] = 1

        self.orange = dict(response_template)
        self.orange["id"] = 2
        self.orange["level"] = "Orange"

        self.EI02 = dict(response_template)
        self.EI02["id"] = 3
        self.EI03 = dict(response_template)
        self.EI03["id"] = 4
        self.EI03["regions"] = ["EI03"]

        self.many_regions = dict(response_template)
        self.many_regions["id"] = 5
        self.many_regions["regions"] = ["EI03", "EI28", "whoop"]

    def test_givenTwoWarningsAndOneDesired_returnOne(self):
        desired_county_codes = ["EI02"]
        parsed_warnings = response_parser.parse_warnings(
            [self.EI02, self.EI03],
            desired_county_codes
        )
        self.assertEqual(len(parsed_warnings), 1)

    def test_givenTwoWarningsOfDifferentLevel_sortBySeverity(self):
        sorted_warnings = response_parser.parse_warnings(
            [self.yellow, self.orange],
            ["EI02"])
        expected = ["Orange", "Yellow"]
        actual = [wg.level for wg in sorted_warnings]
        self.assertEqual(expected, actual)

    def test_givenTwoWarningsOfSameLevel_sortByCounty(self):
        sorted_warnings = response_parser.parse_warnings(
            [self.EI02, self.EI03],
            ["EI03", "EI02"]
        )
        expected = [["EI03"], ["EI02"]]
        actual = [wg.regions for wg in sorted_warnings]
        self.assertEqual(expected, actual)

    def test_givenWarningsWithMultipleRegions_selectCorrectWarnings(self):
        sorted_filtered_warnings = response_parser.parse_warnings(
            [self.many_regions],
            ["EI03"]
        )
        self.assertEqual(len(sorted_filtered_warnings), 1)
        expected = ["EI03", "EI28", "whoop"]
        actual = sorted_filtered_warnings[0].regions
        self.assertEqual(expected, actual)

    def test_givenWarningsMultipleLevelsCounties_sortCountyThenLevel(self):
        sorted_filtered_warnings = response_parser.parse_warnings(
            [self.yellow, self.orange, self.EI02, self.EI03],
            ["EI03", "EI02"]
        )
        expected = (2, 4, 1, 3)
        actual = tuple((wg.id for wg in sorted_filtered_warnings))
        self.assertEqual(expected, actual)