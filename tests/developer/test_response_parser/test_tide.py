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

def test_given_response_as_dict_return_iterable_of_tuples(expected_formatting, response):
    expected = expected_formatting
    actual = parse_tide.generate_tide_rows(response)
    assert expected == actual
