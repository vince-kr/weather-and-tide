import datetime
import unittest

import xmltodict

import config
from response_parser import parse_weather


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
        actual = parse_weather._extract_weather_datums(input_data)
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
        actual = parse_weather._combine_datums(double_tuple)
        self.assertEqual(expected, actual)

    def test_givenSixTenAm_return6_9_12_15(self):
        expected = (
            "6:00 - 9:00",
            "9:00 - 12:00",
            "12:00 - 15:00",
            "15:00 - 18:00",
        )
        actual = parse_weather._calculate_hours(datetime.datetime(2025, 7, 16, 6, 10))
        self.assertEqual(expected, actual)

    def test_givenSixTenPm_return18_21_0_3(self):
        expected = (
            "18:00 - 21:00",
            "21:00 - 0:00",
            "0:00 - 3:00",
            "3:00 - 6:00",
        )
        actual = parse_weather._calculate_hours(datetime.datetime(2025, 7, 16, 18, 10))
        self.assertEqual(expected, actual)

    def test_givenThrupleOfData_returnAverageOfNumericalFields(self):
        selector = parse_weather.Selector(
            data_type="temperature", key="@unit", symbol="° C"
        )
        input_thruple = self.input_data_weather[0]
        expected = "13.4° C"
        actual = parse_weather._average_value(input_thruple, selector)
        self.assertEqual(expected, actual)

    def test_givenHighPrecisionFloat_returnOneDecimalStr(self):
        expected = "3.5"
        actual = parse_weather._avg_and_format(
            (2.12345, 3.56789, 4.86424), lambda x: x
        )
        self.assertEqual(expected, actual)

    def test_givenMetresPerSecond_convertKmPerHour(self):
        expected = "21.6"
        actual = parse_weather._avg_and_format((5, 6, 7), lambda x: x * 3.6)
        self.assertEqual(expected, actual)

    def test_givenThrupleOfData_returnMostCommonString(self):
        selector = parse_weather.Selector("windDirection", "@name", "")
        input_thruple = self.input_data_weather[0]
        expected = "N"
        actual = parse_weather._average_value(input_thruple, selector)
        self.assertEqual(expected, actual)

    def test_givenCollectionOfThruplesOfData_returnTupleOfValues(self):
        selector = parse_weather.Selector("temperature", "@unit", "° C")
        expected = (
            "13.4° C",
            "13.4° C",
            "13.4° C",
        )
        actual = tuple(
            parse_weather._average_value(batch, selector)
            for batch in self.input_data_weather
        )
        self.assertEqual(expected, actual)

    def test_givenMultipleSelectors_returnMultipleTuples(self):
        selectors = (
            parse_weather.Selector("temperature", "@unit", "° C"),
            parse_weather.Selector("windDirection", "@name", ""),
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
                    parse_weather._average_value(batch, sel)
                    for batch in self.input_data_weather
                )
            )
        actual = tuple(results)
        self.assertEqual(expected, actual)

    def test_parseEndToEnd(self):
        expected = self.expected_formatting
        forecast_fmt = parse_weather.generate_weather_rows(self.response)
        actual = tuple(row_data for _, row_data in forecast_fmt)
        # self.assertEqual(expected, actual)

