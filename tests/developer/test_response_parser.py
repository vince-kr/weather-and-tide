"""Create a module to convert API responses into useful objects"""

import json
import unittest

import config
import response_parser
import xmltodict


class TestTide(unittest.TestCase):
    def setUp(self):
        self.datetimestamp = "2024-09-26T18:31:00+00:00"
        with open(config.PROJECT_ROOT / "tests/cached_api_responses/tide.json") as tf:
            self.response = json.load(tf)
        self.expected_formatting = (
            (
                "Low",
                ("05:17",),
            ),
            (
                "High",
                ("11:46",),
            ),
            (
                "Low",
                ("17:32",),
            ),
            (
                "High",
                ("23:57",),
            ),
        )

    def test_sanity(self):
        self.assertTrue(True)

    def test_givenBigDateTimeString_extractOnlyTimeInLocalZone(self):
        expected = "19:31"
        actual = response_parser._extract_time_from(self.datetimestamp)
        self.assertEqual(expected, actual)

    def test_givenResponseAsDict_returnIterableOfTuples(self):
        expected = self.expected_formatting
        actual = response_parser._generate_tide_rows(self.response)
        self.assertEqual(expected, actual)

    def test_parseEndToEnd(self):
        expected = self.expected_formatting
        actual = response_parser.parse_forecast(self.response)
        self.assertEqual(expected, actual)


# noinspection PyArgumentList
class TestWeather(unittest.TestCase):
    def setUp(self):
        with open(config.PROJECT_ROOT / "tests/cached_api_responses/weather.xml") as wf:
            self.response = xmltodict.parse(wf.read())
        self.expected_formatting = (
            (
                "11.6° C",
                "12.3° C",
                "12.5° C",
                "12.2° C",
            ),
            (
                "0.0 mm",
                "0.0 mm",
                "0.0 mm",
                "0.0 mm",
            ),
            (
                "4.9 km/h",
                "4.7 km/h",
                "5.9 km/h",
                "7.8 km/h",
            ),
            (
                "SW",
                "S",
                "SE",
                "SE",
            ),
            (
                "99.8%",
                "99.3%",
                "100.0%",
                "97.7%",
            ),
        )
        self.input_data_weather = (
            (
                {"temperature": {"@unit": "12.4"}, "windDirection": {"@name": "N"}},
                {"temperature": {"@unit": "13.4"}, "windDirection": {"@name": "N"}},
                {"temperature": {"@unit": "14.4"}, "windDirection": {"@name": "N"}},
            ),
            (
                {"temperature": {"@unit": "12.4"}, "windDirection": {"@name": "N"}},
                {"temperature": {"@unit": "13.4"}, "windDirection": {"@name": "N"}},
                {"temperature": {"@unit": "14.4"}, "windDirection": {"@name": "N"}},
            ),
            (
                {"temperature": {"@unit": "12.4"}, "windDirection": {"@name": "N"}},
                {"temperature": {"@unit": "13.4"}, "windDirection": {"@name": "N"}},
                {"temperature": {"@unit": "14.4"}, "windDirection": {"@name": "N"}},
            ),
        )
        self.input_data_precip = (
            (
                {"precipitation": {"@value": "2"}},
                {"precipitation": {"@value": "3"}},
                {"precipitation": {"@value": "4"}},
            ),
            (
                {"precipitation": {"@value": "2"}},
                {"precipitation": {"@value": "3"}},
                {"precipitation": {"@value": "4"}},
            ),
            (
                {"precipitation": {"@value": "2"}},
                {"precipitation": {"@value": "3"}},
                {"precipitation": {"@value": "4"}},
            ),
        )

    def test_sanity(self):
        self.assertTrue(True)

    def test_givenResponseAsDict_returnPertinentDataPoints(self):
        input_data = [{"location": count} for count in range(10)]
        expected = (0, 2, 4, 6), (3, 5, 7, 9)
        actual = response_parser._extract_weather_datums(input_data)
        self.assertEqual(expected, actual)

    def test_givenTwoTuplesOfDicts_returnSingleTupleCombined(self):
        double_tuple = self.input_data_weather[0], self.input_data_precip[0]
        expected = (
            {
                "temperature": {"@unit": "12.4"},
                "windDirection": {"@name": "N"},
                "precipitation": {"@value": "2"},
            },
            {
                "temperature": {"@unit": "13.4"},
                "windDirection": {"@name": "N"},
                "precipitation": {"@value": "3"},
            },
            {
                "temperature": {"@unit": "14.4"},
                "windDirection": {"@name": "N"},
                "precipitation": {"@value": "4"},
            },
        )
        actual = response_parser._combine_datums(double_tuple)
        self.assertEqual(expected, actual)

    def test_givenThrupleOfData_returnAverageOfNumericalFields(self):
        selector = response_parser.Selector(
            data_type="temperature", key="@unit", symbol="° C"
        )
        input_thruple = self.input_data_weather[0]
        expected = "13.4° C"
        actual = response_parser._average_value(input_thruple, selector)
        self.assertEqual(expected, actual)

    def test_givenHighPrecisionFloat_returnOneDecimalStr(self):
        expected = "3.5"
        actual = response_parser._avg_and_format(
            (2.12345, 3.56789, 4.86424), lambda x: x
        )
        self.assertEqual(expected, actual)

    def test_givenMetresPerSecond_convertKmperHour(self):
        expected = "21.6"
        actual = response_parser._avg_and_format((5, 6, 7), lambda x: x * 3.6)
        self.assertEqual(expected, actual)

    def test_givenThrupleOfData_returnMostCommonString(self):
        selector = response_parser.Selector("windDirection", "@name", "")
        input_thruple = self.input_data_weather[0]
        expected = "N"
        actual = response_parser._average_value(input_thruple, selector)
        self.assertEqual(expected, actual)

    def test_givenCollectionOfThruplesOfData_returnTupleOfValues(self):
        selector = response_parser.Selector("temperature", "@unit", "° C")
        expected = (
            "13.4° C",
            "13.4° C",
            "13.4° C",
        )
        actual = tuple(
            response_parser._average_value(batch, selector)
            for batch in self.input_data_weather
        )
        self.assertEqual(expected, actual)

    def test_givenMultipleSelectors_returnMultipleTuples(self):
        selectors = (
            response_parser.Selector("temperature", "@unit", "° C"),
            response_parser.Selector("windDirection", "@name", ""),
        )
        expected = (
            (
                "13.4° C",
                "13.4° C",
                "13.4° C",
            ),
            (
                "N",
                "N",
                "N",
            ),
        )
        results = []
        for sel in selectors:
            results.append(
                tuple(
                    response_parser._average_value(batch, sel)
                    for batch in self.input_data_weather
                )
            )
        actual = tuple(results)
        self.assertEqual(expected, actual)

    def test_parseEndToEnd(self):
        expected = self.expected_formatting
        forecast_fmt = response_parser.parse_forecast(self.response)
        actual = tuple(row_data for _, row_data in forecast_fmt)
        self.assertEqual(expected, actual)


class TestWarning(unittest.TestCase):
    def setUp(self):
        with open(
            config.PROJECT_ROOT / "tests/cached_api_responses/warnings.json"
        ) as wf:
            self.response: list[dict] = json.load(wf)
        with open(config.PROJECT_ROOT / "county_to_fips.json") as cf:
            self.COUNTIES_TO_FIPS: dict[str, str] = json.load(cf)

    def test_givenSixWarnings_onlySelectForClareOrGalway(self):
        desired_counties = {"Clare", "Galway"}
        expected = [self.response[idx] for idx in (0, 1, 2, 6)]
        actual = response_parser._select_counties(
            self.response, desired_counties, self.COUNTIES_TO_FIPS
        )
        self.assertEqual(expected, actual)

    def test_givenCompleteWarnings_onlySelectDesiredData(self):
        expected = {
            "level": "Yellow",
            "headline": "Rain warning for Clare, Connacht, "
            "Donegal, Cavan, Monaghan, Longford, "
            "Louth, Meath, Westmeath",
            "onset": "2024-12-06T16:52:23-00:00",
            "expiry": "2024-12-07T10:00:00-00:00",
            "description": "Storm Darragh: heavy rain on Friday followed by heavy showers Saturday morning.  Potential impacts:  • Localised flooding • Poor visibility • Difficult travelling conditions ",
        }
        actual = response_parser._filter_keys(self.response[0])
        self.assertEqual(expected, actual)
