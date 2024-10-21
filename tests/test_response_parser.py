"""Create a module to convert API responses into useful objects"""
import json
import response_parser
import unittest
import xmltodict


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


class TestWeather(unittest.TestCase):
    def setUp(self):
        with open('cached_api_responses/weather.xml') as wf:
            self.response: dict = xmltodict.parse(wf.read())
        self.expected_formatting = (
            (
                "9.1° C",
                "9.2° C",
                "8.3° C",
                "7.5° C",
            ),
            (
                "0 mm",
                "0.7 mm",
                "1.7 mm",
                "2.2 mm",
            ),
            (
                "24.6 km/h",
                "25.2 km/h",
                "31.1 km/h",
                "36.2 km/h",
            ),
            (
                "N",
                "N",
                "N",
                "N",
            ),
            (
                "98.5%",
                "100.0",
                "100.0",
                "100.0",
            ),
        )
        self.input_data = (
            (
                {
                    "temperature": {
                        "@unit": "12.4"
                    },
                    "windDirection": {
                        "@name": "N"
                    }
                },
                {
                    "temperature": {
                        "@unit": "13.4"
                    },
                    "windDirection": {
                        "@name": "N"
                    }
                },
                {
                    "temperature": {
                        "@unit": "14.4"
                    },
                    "windDirection": {
                        "@name": "N"
                    }
                },
            ),
            (
                {
                    "temperature": {
                        "@unit": "12.4"
                    },
                    "windDirection": {
                        "@name": "N"
                    }
                },
                {
                    "temperature": {
                        "@unit": "13.4"
                    },
                    "windDirection": {
                        "@name": "N"
                    }
                },
                {
                    "temperature": {
                        "@unit": "14.4"
                    },
                    "windDirection": {
                        "@name": "N"
                    }
                },
            ),
            (
                {
                    "temperature": {
                        "@unit": "12.4"
                    },
                    "windDirection": {
                        "@name": "N"
                    }
                },
                {
                    "temperature": {
                        "@unit": "13.4"
                    },
                    "windDirection": {
                        "@name": "N"
                    }
                },
                {
                    "temperature": {
                        "@unit": "14.4"
                    },
                    "windDirection": {
                        "@name": "N"
                    }
                },
            )
        )

    def test_sanity(self):
        self.assertTrue(True)

    def test_givenResponseAsDict_returnPertinentDataPoints(self):
        input_data = [{"location": count} for count in range(10)]
        expected = (0, 2, 4, 6), (3, 5, 7, 9)
        actual = response_parser._extract_weather_datums(input_data)
        self.assertEqual(expected, actual)

    def test_givenThrupleOfData_returnAverageOfNumericalFields(self):
        selector = response_parser.Selector(
            data_type="temperature",
            key="@unit",
            symbol="° C"
        )
        input_thruple = self.input_data[0]
        expected = "13.4° C"
        actual = response_parser._average_value(input_thruple, selector)
        self.assertEqual(expected, actual)

    def test_givenThrupleOfData_returnMostCommonString(self):
        selector = response_parser.Selector(
            "windDirection",
            "@name",
            ""
        )
        input_thruple = self.input_data[0]
        expected = "N"
        actual = response_parser._average_value(input_thruple, selector)
        self.assertEqual(expected, actual)

    def test_givenCollectionOfThruplesOfData_returnTupleOfValues(self):
        selector = response_parser.Selector(
            "temperature",
            "@unit",
            "° C"
        )
        expected = (
            "13.4° C",
            "13.4° C",
            "13.4° C",
        )
        actual = tuple(response_parser._average_value(batch, selector)
                       for batch in self.input_data)
        self.assertEqual(expected, actual)

    def test_givenMultipleSelectors_returnMultipleTuples(self):
        selectors = (
            response_parser.Selector(
                "temperature",
                "@unit",
                "° C"
            ),
            response_parser.Selector(
                "windDirection",
                "@name",
                ""
            )
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
            )
        )
        results = []
        for sel in selectors:
            results.append(tuple(response_parser._average_value(batch, sel)
                                 for batch in self.input_data))
        actual = tuple(results)
        self.assertEqual(expected, actual)

    def SKIPtest_wthXML(self):
        """Build a JSON representation of weather data"""
        forecasts = self.response['weatherdata']['product']['time']
        weather, precip = response_parser._extract_weather_datums(forecasts[:26])
        print(weather)
        with open('really.json', 'w') as rf:
            json.dump(weather, rf, indent=4)
