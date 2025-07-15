import datetime
from collections import Counter, namedtuple
import itertools
from operator import attrgetter
from typing import Callable, Generator, Literal, Sequence

from pydantic import BaseModel

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


class WeatherWarning(BaseModel):
    id: int
    level: Literal["Red", "Orange", "Yellow"]
    headline: str
    onset: datetime.datetime
    expiry: datetime.datetime
    description: str
    regions: list[str]

    @property
    def level_index(self) -> int:
        return ("Red", "Orange", "Yellow").index(self.level)

def parse_warnings(
        warnings_response: list[dict],
        desired_fips: list[str]
) -> list[WeatherWarning]:
    warning_objects = (WeatherWarning.model_validate(raw_warning)
                       for raw_warning in warnings_response)
    filtered_wgs = (wg for wg in warning_objects
                    if set(wg.regions) & set(desired_fips))
    sorted_county = _sort_by_county(filtered_wgs, desired_fips)
    sorted_level = sorted(sorted_county, key=attrgetter("level_index"))
    return sorted_level[:4]
    

def _sort_by_county(
        warnings: Generator[WeatherWarning, None, None],
        desired_fips: list[str]
) -> list[WeatherWarning]:
    county_order = {code: i for i, code in enumerate(desired_fips)}

    def sort_key(wg: WeatherWarning):
        valid_codes = (county_order[code] for code in wg.regions
                       if code in county_order)
        return min(valid_codes)

    return sorted(warnings, key=sort_key)


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
                for datum in _batched(all_datums, 3)
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


def _batched(data: Sequence, length: int) -> Generator:
    iterator = iter(data)
    while batch := tuple(itertools.islice(iterator, length)):
        yield batch


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
