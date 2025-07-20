import json

import pytest

import config
from response_parser import parse_tide


@pytest.fixture
def timestamp():
    return "2024-09-26T18:31:00+00:00"

@pytest.fixture
def response():
    with open(config.PROJECT_ROOT / "tests/cached_api_responses/tide.json") as tf:
        return json.load(tf)

@pytest.fixture
def expected_formatting():
    return (
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

def test_givenBigDateTimeString_extractOnlyTimeInLocalZone(timestamp):
    expected = "19:31"
    actual = parse_tide._extract_time_from(timestamp)
    assert expected == actual

def test_givenResponseAsDict_returnIterableOfTuples(expected_formatting, response):
    expected = expected_formatting
    actual = parse_tide.generate_tide_rows(response)
    assert expected == actual
