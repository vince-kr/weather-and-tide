import datetime

import pytest
import xmltodict

import config
from response_parser import parse_weather


@pytest.fixture
def cached_response():
    with open(config.PROJECT_ROOT / "tests/cached_api_responses/weather.xml") as wf:
        response = xmltodict.parse(wf.read())
    return response


def test_sanity():
    assert 1 == True

def test_givenResponseAsDict_returnPertinentDataPoints():
    input_data = range(10)
    expected = (0, 2, 4, 6), (3, 5, 7, 9)
    actual = parse_weather._split_by_index(input_data)
    assert expected == actual

def test_givenSixTenAm_return6_9_12_15():
    expected = (
        "6:00 - 9:00",
        "9:00 - 12:00",
        "12:00 - 15:00",
        "15:00 - 18:00",
    )
    actual = parse_weather._calculate_hours(datetime.datetime(2025, 7, 16, 6, 10))
    assert expected == actual

def test_givenSixTenPm_return18_21_0_3():
    expected = (
        "18:00 - 21:00",
        "21:00 - 0:00",
        "0:00 - 3:00",
        "3:00 - 6:00",
    )
    actual = parse_weather._calculate_hours(datetime.datetime(2025, 7, 16, 18, 10))
    assert expected == actual

@pytest.fixture
def current_hours():
    return parse_weather._calculate_hours(datetime.datetime.now())

def test_givenCachedResponse_returnWeatherRows(cached_response, current_hours):
    expected = current_hours, (
        "11.6° C",
        "12.3° C",
        "12.5° C",
        "12.2° C",
    ), (
        "0.0 mm",
        "0.0 mm",
        "0.0 mm",
        "0.0 mm",
    ), (
        "4.9 km/h",
        "4.7 km/h",
        "5.9 km/h",
        "7.8 km/h",
    ), (
        "SW",
        "S",
        "SE",
        "SE",
    ), (
        "99.8%",
        "99.3%",
        "100.0%",
        "97.7%",
    )
    headers_rows = parse_weather.generate_weather_rows(cached_response)
    actual = tuple(rows for _, rows in headers_rows)
    assert expected == actual
