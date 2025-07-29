import pytest

from response_parser import parse_warning


@pytest.fixture
def response_template():
    return dict(
        id=0,
        level="Yellow",
        headline="Scary weather warning!",
        onset="2024-09-26T18:31:00+00:00",
        expiry="2024-09-27T18:31:00+00:00",
        description="Impacts: • Difficult travel conditions • Localised flooding",
        regions=["EI02"]
    )

@pytest.fixture
def warning_levels(response_template):
    yellow = dict(response_template)
    yellow["id"] = 1

    orange = dict(response_template)
    orange["id"] = 2
    orange["level"] = "Orange"

    return {
        "yellow": yellow,
        "orange": orange,
    }

@pytest.fixture
def warning_regions(response_template):
    EI02 = dict(response_template)
    EI02["id"] = 3

    EI03 = dict(response_template)
    EI03["id"] = 4
    EI03["regions"] = ["EI03"]

    return {
        "EI02": EI02,
        "EI03": EI03,
    }

@pytest.fixture
def warning_many(response_template):
    many_regions = dict(response_template)
    many_regions["id"] = 5
    many_regions["regions"] = ["EI03", "EI28", "whoop"]

    return many_regions

def test_givenTwoWarningsAndOneDesired_returnOne(warning_regions):
    desired_county_codes = ["EI02"]
    parsed_warnings = parse_warning.generate_warnings(
        [warning_regions["EI02"], warning_regions["EI03"]],
        desired_county_codes
    )
    assert len(parsed_warnings) == 1

def test_givenTwoWarningsOfDifferentLevel_sortBySeverity(warning_levels):
    sorted_warnings = parse_warning.generate_warnings(
        [warning_levels["yellow"], warning_levels["orange"]],
        ["EI02"])
    expected = ["Orange", "Yellow"]
    actual = [wg.level for wg in sorted_warnings]
    assert expected == actual

def test_givenTwoWarningsOfSameLevel_sortByCounty(warning_regions):
    sorted_warnings = parse_warning.generate_warnings(
        [warning_regions["EI02"], warning_regions["EI03"]],
        ["EI03", "EI02"]
    )
    expected = [["EI03"], ["EI02"]]
    actual = [wg.regions for wg in sorted_warnings]
    assert expected == actual

def test_givenWarningsWithMultipleRegions_selectCorrectWarnings(warning_many):
    sorted_filtered_warnings = parse_warning.generate_warnings(
        [warning_many],
        ["EI03"]
    )
    assert len(sorted_filtered_warnings) == 1
    expected = ["EI03", "EI28", "whoop"]
    actual = sorted_filtered_warnings[0].regions
    assert expected == actual

def test_sort_county_then_level(warning_levels, warning_regions):
    sorted_filtered_warnings = parse_warning.generate_warnings(
        [
            warning_levels["yellow"],
            warning_levels["orange"],
            warning_regions["EI02"],
            warning_regions["EI03"],
        ],
        ["EI03", "EI02"]
    )
    expected = (2, 4, 1, 3)
    actual = tuple((wg.id for wg in sorted_filtered_warnings))
    assert expected == actual

def test_format_warning_impacts():
    raw_warning_string = "Impacts: • Difficult travel conditions • Localised flooding"
    expected = "Impacts:\n• Difficult travel conditions\n• Localised flooding"
    actual = parse_warning.format_warning_impact(raw_warning_string)
    assert expected == actual

def test_description_is_formatted(warning_levels):
    fmt_warnings = parse_warning.generate_warnings(
        [warning_levels["yellow"], warning_levels["orange"]],
        ["EI02"]
    )
    expected = "Impacts:\n• Difficult travel conditions\n• Localised flooding"
    actual = fmt_warnings[0].description
    assert expected == actual
