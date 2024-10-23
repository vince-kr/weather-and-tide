"""Create a module to convert API responses into useful objects"""
import json
import response_parser
import unittest
import xmltodict


class TestTide(unittest.TestCase):
    def setUp(self):
        self.datetimestamp = "2024-09-26T18:31:00+00:00"
        with open("../cached_api_responses/tide.json") as tf:
            self.response: dict = json.load(tf)

    def test_sanity(self):
        self.assertTrue(True)

    def test_givenBigDateTimeString_extractOnlyTimeInLocalZone(self):
        expected = "19:31"
        actual = response_parser._extract_time_from(self.datetimestamp)
        self.assertEqual(expected, actual)

    def test_givenResponseAsDict_returnIterableOfTuples(self):
        expected = (
            (
                "Low",
                ("19:31",),
            ),
            (
                "High",
                ("01:49",),
            ),
            (
                "Low",
                ("08:07",),
            ),
        )
        actual = response_parser.generate_tide_rows(self.response)
        self.assertEqual(expected, actual)


# noinspection PyArgumentList
class TestWeather(unittest.TestCase):
    def setUp(self):
        with open('../cached_api_responses/weather.xml') as wf:
            self.response: dict = xmltodict.parse(wf.read())
        self.expected_formatting = (
            (
                "9.1° C",
                "9.2° C",
                "8.3° C",
                "7.5° C",
            ),
            (
                "0.0 mm",
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
                "100.0%",
                "100.0%",
                "100.0%",
            ),
        )
        self.input_data_weather = (
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
        self.input_data_precip = (
            (
                {
                    "precipitation": {
                        "@value": "2"
                    }
                },
                {
                    "precipitation": {
                        "@value": "3"
                    }
                },
                {
                    "precipitation": {
                        "@value": "4"
                    }
                },
            ),
            (
                {
                    "precipitation": {
                        "@value": "2"
                    }
                },
                {
                    "precipitation": {
                        "@value": "3"
                    }
                },
                {
                    "precipitation": {
                        "@value": "4"
                    }
                },
            ),
            (
                {
                    "precipitation": {
                        "@value": "2"
                    }
                },
                {
                    "precipitation": {
                        "@value": "3"
                    }
                },
                {
                    "precipitation": {
                        "@value": "4"
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

    def test_givenTwoTuplesOfDicts_returnSingleTupleCombined(self):
        double_tuple = self.input_data_weather[0], self.input_data_precip[0]
        expected = (
            {
                "temperature": {
                    "@unit": "12.4"
                },
                "windDirection": {
                    "@name": "N"
                },
                "precipitation": {
                    "@value": "2"
                }
            },
            {
                "temperature": {
                    "@unit": "13.4"
                },
                "windDirection": {
                    "@name": "N"
                },
                "precipitation": {
                    "@value": "3"
                }
            },
            {
                "temperature": {
                    "@unit": "14.4"
                },
                "windDirection": {
                    "@name": "N"
                },
                "precipitation": {
                    "@value": "4"
                }
            },
        )
        actual = response_parser._combine_datums(double_tuple)
        self.assertEqual(expected, actual)

    def test_givenThrupleOfData_returnAverageOfNumericalFields(self):
        selector = response_parser.Selector(
            data_type="temperature",
            key="@unit",
            symbol="° C"
        )
        input_thruple = self.input_data_weather[0]
        expected = "13.4° C"
        actual = response_parser._average_value(input_thruple, selector)
        self.assertEqual(expected, actual)

    def test_givenHighPrecisionFloat_returnOneDecimalStr(self):
        expected = "3.5"
        actual = response_parser._avg_and_format((2.12345, 3.56789, 4.86424), lambda x: x)
        self.assertEqual(expected, actual)

    def test_givenMetresPerSecond_convertKmperHour(self):
        expected = "21.6"
        actual = response_parser._avg_and_format((5, 6, 7), lambda x: x*3.6)
        self.assertEqual(expected, actual)

    def test_givenThrupleOfData_returnMostCommonString(self):
        selector = response_parser.Selector(
            "windDirection",
            "@name",
            ""
        )
        input_thruple = self.input_data_weather[0]
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
                       for batch in self.input_data_weather)
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
                                 for batch in self.input_data_weather))
        actual = tuple(results)
        self.assertEqual(expected, actual)

    def test_fullParse(self):
        expected = self.expected_formatting
        actual = response_parser.generate_weather_rows(self.response)[1]
        self.assertEqual(expected, actual)