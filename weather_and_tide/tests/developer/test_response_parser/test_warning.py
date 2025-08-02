import pytest

from weather_and_tide.response_parser import parse_warning


@pytest.fixture
def response_template():
    return parse_warning.WeatherWarning.model_validate(dict(
        id=0,
        level="Yellow",
        headline="Scary weather warning!",
        onset="2024-09-26T18:31:00+00:00",
        expiry="2024-09-27T18:31:00+00:00",
        description="Impacts: • Difficult travel conditions • Localised flooding",
        regions=["EI02"]
    ))

@pytest.fixture
def warning_levels(response_template):
    yellow = response_template.model_copy()
    yellow.id = 1

    orange = response_template.model_copy()
    orange.id = 2
    orange.level = "Orange"

    return {
        "yellow": yellow,
        "orange": orange,
    }

@pytest.fixture
def warning_regions(response_template):
    EI02 = response_template.model_copy()
    EI02.id = 3

    EI03 = response_template.model_copy()
    EI03.id = 4
    EI03.regions = ["EI03"]

    return {
        "EI02": EI02,
        "EI03": EI03,
    }

@pytest.fixture
def warning_many(response_template):
    many_regions = response_template.model_copy()
    many_regions.id = 5
    many_regions.regions = ["EI03", "EI28", "whoop"]

    return many_regions

def test_given_two_warnings_and_one_desired_return_one(warning_regions):
    desired_county_codes = ["EI02"]
    warnings_list = parse_warning.WeatherWarningsList(
        [
            warning_regions["EI02"],
            warning_regions["EI03"],
        ],
        desired_county_codes
    )
    filtered = warnings_list.filter_by_county()
    assert len(filtered) == 1

def test_given_two_warnings_of_different_level_sort_by_severity(warning_levels):
    warnings_list = parse_warning.WeatherWarningsList(
        [warning_levels["yellow"], warning_levels["orange"]],
        ["EI02"])
    expected = ["Orange", "Yellow"]
    sorted_wgs = warnings_list.sort_by_severity()
    actual = [wg.level for wg in sorted_wgs]
    assert actual == expected

def test_given_two_warnings_of_same_level_sort_by_county(warning_regions):
    warnings_list = parse_warning.WeatherWarningsList(
        [warning_regions["EI02"], warning_regions["EI03"]],
        ["EI03", "EI02"]
    )
    sorted_wgs = warnings_list.sort_by_county()
    expected = [["EI03"], ["EI02"]]
    actual = [wg.regions for wg in sorted_wgs]
    assert actual == expected

def test_given_warnings_with_multiple_regions_select_correct_warnings(warning_many):
    warnings_list = parse_warning.WeatherWarningsList(
        [warning_many],
        ["EI03"]
    )
    assert len(warnings_list) == 1
    expected = ["EI03", "EI28", "whoop"]
    actual = warnings_list[0].regions
    assert actual == expected

def test_sort_county_then_level(warning_levels, warning_regions):
    warnings_list = parse_warning.WeatherWarningsList(
        [
            warning_levels["yellow"],
            warning_levels["orange"],
            warning_regions["EI02"],
            warning_regions["EI03"],
        ],
        ["EI03", "EI02"]
    )
    fs_wgs = warnings_list.filter_by_county().sort_by_county().sort_by_severity()
    expected = (2, 4, 1, 3)
    actual = tuple((wg.id for wg in fs_wgs))
    assert actual == expected
