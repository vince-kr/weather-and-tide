from collections import Counter, namedtuple
import datetime
import itertools
from typing import Callable, Generator, Sequence

Selector = namedtuple(
    "Selector", "data_type key symbol conversion", defaults=[lambda x: x]
)

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
    "",
    "Temperature",
    "Precipitation",
    "Wind speed",
    "Wind direction",
    "Cloud cover",
)

def generate_weather_rows(weather: dict) -> zip:
    forecasts = weather["weatherdata"]["product"]["time"]
    temp_wind, precip = _extract_weather_datums(forecasts[:26])
    all_datums = _combine_datums((temp_wind, precip))
    hours = _calculate_hours(datetime.datetime.now())
    average_values = []
    for selector in weather_selectors:
        average_values.append(
            tuple(
                _average_value(datum, selector)
                for datum in _batched(all_datums, 3)
            )
        )
    rows = [hours] + average_values
    return zip(weather_row_headers, tuple(rows))


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


def _calculate_hours(current_time: datetime.datetime) -> tuple[str, ...]:
    datetime_objects = ((current_time + datetime.timedelta(hours=i))
                         for i in (0, 3, 6, 9, 12))
    hours_fmt = (f"{start.hour}:00 - {stop.hour}:00"
                 for start, stop in itertools.pairwise(datetime_objects))
    return tuple(hours_fmt)


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

