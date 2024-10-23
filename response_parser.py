from collections import Counter, namedtuple
from collections.abc import Iterable
import itertools
from typing import Callable, Sequence

"""
All of the below may be useful once I start implementing weather
import xml.etree.ElementTree as ET

def select_forecasts(weather_api_data: ET) -> list[ET.Element]:
    weather_data_root = weather_api_data.getroot()
    forecasts = weather_data_root[1]
    required_forecast_hours = 15
    datapoints_per_hour = 2
    total_datapoints = required_forecast_hours * datapoints_per_hour
    return forecasts[:total_datapoints]

class Forecast:
    def __init__(self, forecast: ET.Element):
        self.temperature = forecast[0][0].attrib['value']
        self.temp_unit = forecast[0][0].attrib['unit']
        self.wind_speed = forecast[0][2].attrib['mps']
"""

Selector = namedtuple('Selector',
                      'data_type key symbol conversion',
                      defaults=[lambda x: x])

# noinspection PyArgumentList
weather_selectors = (
    Selector(
        "temperature",
        "@value",
        "° C",
    ),
    Selector(
        "precipitation",
        "@value",
        " mm"
    ),
    Selector(
        "windSpeed",
        "@mps",
        " km/h",
        lambda x: x * 3.6
    ),
    Selector(
        "windDirection",
        "@name",
        ""
    ),
    Selector(
        "cloudiness",
        "@percent",
        "%"
    )
)

weather_row_headers = (
    "Temperature",
    "Precipitation",
    "Wind speed",
    "Wind direction",
    "Cloud cover",
)

def generate_tide_rows(tides: dict) -> tuple:
    return tuple(
        (
            tide_datum['type'].capitalize(),
            tuple((_extract_time_from(tide_datum['time']),))
        )
        for tide_datum in tides['data']
    )

def _extract_time_from(datetimestamp: str) -> str:
    return datetimestamp[11:16]

def generate_weather_rows(weather: dict) -> tuple:
    forecasts = weather['weatherdata']['product']['time']
    temp_wind, precip = _extract_weather_datums(forecasts[:26])
    all_datums = _combine_datums((temp_wind, precip))
    average_values = []
    for selector in weather_selectors:
        average_values.append(tuple(_average_value(datum, selector)
                               for datum in itertools.batched(all_datums, n=3)))
    return weather_row_headers, tuple(average_values)


def _extract_weather_datums(all_data: Iterable) -> tuple:
    """Given an iterable, return a 2-tuple of tuples that contain
    - all even indices from the iterable minus the last one
    - all odd indices from the iterable minus the first one
    """
    weather = tuple(point['location'] for idx, point in enumerate(all_data[:-2])
                  if _is_even(idx))
    precip = tuple(point['location'] for idx, point in enumerate(all_data[2:])
                 if not _is_even(idx))
    return weather, precip

def _is_even(number: int) -> bool:
    return number % 2 == 0

def _combine_datums(datums: tuple) -> tuple:
    return tuple(weather | precip for weather, precip in zip(*datums))

def _average_value(data: tuple, selector: Selector) -> str:
    pertinent_values = [point[selector.data_type][selector.key]
                        for point in data]
    try:
        fmt = _avg_and_format(pertinent_values, selector.conversion)
    except ValueError:
        fmt = Counter(pertinent_values).most_common()[0][0]
    return f'{fmt}{selector.symbol}'

def _avg_and_format(values: Sequence, conversion: Callable) -> str:
    average = sum(float(point) for point in values) / len(values)
    return f'{conversion(average):.1f}'