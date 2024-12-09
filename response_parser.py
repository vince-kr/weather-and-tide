import datetime
from collections import Counter, namedtuple
import itertools
from typing import Callable, Sequence

Selector = namedtuple(
    "Selector", "data_type key symbol conversion", defaults=[lambda x: x]
)

# noinspection PyArgumentList
weather_selectors = (
    Selector(
        "temperature",
        "@value",
        "° C",
    ),
    Selector("precipitation", "@value", " mm"),
    Selector("windSpeed", "@mps", " km/h", lambda x: x * 3.6),
    Selector("windDirection", "@name", ""),
    Selector("cloudiness", "@percent", "%"),
)

weather_row_headers = (
    "Temperature",
    "Precipitation",
    "Wind speed",
    "Wind direction",
    "Cloud cover",
)


def format_warnings(
    warnings: list[dict], desired_counties: set[str], counties_to_fips: dict[str, str]
) -> list[dict]:
    desired_warnings: list[dict] = _select_counties(
        warnings, desired_counties, counties_to_fips
    )
    desired_data = [_filter_keys(warning) for warning in desired_warnings]
    for warning in desired_data:
        warning["onset"] = _format_warning_timestamps(warning["onset"])
        warning["expiry"] = _format_warning_timestamps(warning["expiry"])
    return desired_data


def _select_counties(
    warnings: list[dict], desired_counties: set[str], counties_to_fips: dict[str, str]
) -> list[dict] | None:
    desired_county_codes = set(
        counties_to_fips[county_name] for county_name in desired_counties
    )
    matching_warnings = [
        warning
        for warning in warnings
        if set(warning["regions"]) & desired_county_codes
    ]
    return matching_warnings


def _filter_keys(warning: dict[str, str]) -> dict[str, str]:
    return {
        key: warning[key]
        for key in ("level", "headline", "onset", "expiry", "description")
    }


def _format_warning_timestamps(raw_timestamp: str) -> str:
    as_object = datetime.datetime.fromisoformat(raw_timestamp)
    return as_object.strftime("%-d %B, %H:%M")


def format_moon_phase(phase_data: dict) -> str:
    return f"{phase_data['phaseEmoji']} {phase_data['phase']}"


def parse_forecast(forecast: dict) -> zip | tuple:
    if "weatherdata" in forecast:
        return _generate_weather_rows(forecast)
    else:
        return _generate_tide_rows(forecast)


def _generate_weather_rows(weather: dict) -> zip:
    forecasts = weather["weatherdata"]["product"]["time"]
    temp_wind, precip = _extract_weather_datums(forecasts[:26])
    all_datums = _combine_datums((temp_wind, precip))
    average_values = []
    for selector in weather_selectors:
        average_values.append(
            tuple(
                _average_value(datum, selector)
                for datum in itertools.batched(all_datums, n=3)
            )
        )
    return zip(weather_row_headers, tuple(average_values))


def _extract_weather_datums(all_data: Sequence) -> tuple:
    """Given an iterable, return a 2-tuple of tuples that contain
    - all even indices from the iterable minus the last one
    - all odd indices from the iterable minus the first one
    """
    weather = tuple(
        point["location"] for idx, point in enumerate(all_data[:-2]) if _is_even(idx)
    )
    precip = tuple(
        point["location"] for idx, point in enumerate(all_data[2:]) if not _is_even(idx)
    )
    return weather, precip


def _is_even(number: int) -> bool:
    return number % 2 == 0


def _combine_datums(datums: tuple) -> tuple:
    return tuple(weather | precip for weather, precip in zip(*datums))


def _average_value(data: tuple, selector: Selector) -> str:
    pertinent_values = [point[selector.data_type][selector.key] for point in data]
    try:
        fmt = _avg_and_format(pertinent_values, selector.conversion)
    except ValueError:
        fmt = Counter(pertinent_values).most_common()[0][0]
    return f"{fmt}{selector.symbol}"


def _avg_and_format(values: Sequence, conversion: Callable) -> str:
    average = sum(float(point) for point in values) / len(values)
    return f"{conversion(average):.1f}"


def _generate_tide_rows(tides: dict) -> tuple:
    return tuple(
        (
            tide_datum["type"].capitalize(),
            tuple((_extract_time_from(tide_datum["time"]),)),
        )
        for tide_datum in tides["data"]
    )


def _extract_time_from(datetimestamp: str) -> str:
    utc_time = datetime.datetime.fromisoformat(datetimestamp)
    return utc_time.astimezone(tz=None).strftime("%H:%M")
