from collections import Counter, namedtuple
from collections.abc import Iterable
import itertools
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

Selector = namedtuple('Selector', ['data_type', 'key', 'symbol'])

def format_tide_response(tides: dict) -> tuple:
    return tuple(
        (
            tide_datum['type'].capitalize(),
            tuple((_extract_time_from(tide_datum['time']),))
        )
        for tide_datum in tides['data']
    )

def _extract_time_from(datetimestamp: str) -> str:
    return datetimestamp[11:16]

def format_weather_response(weather: dict) -> tuple:
    forecasts = weather['weatherdata']['product']['time']
    weather, precip = _extract_weather_datums(forecasts[:26])
    weather_batches = itertools.batched(weather, n=3)
    precip_batches = itertools.batched(precip, n=3)
    for weather_point, precip_point in zip(weather_batches, precip_batches):
        pass


def _extract_weather_datums(all_data: Iterable) -> tuple:
    """Given an iterable, return a 2-tuple of tuples that contain
    - all even indices from the iterable minus the last one
    - all odd indices from the iterable minus the first one
    """
    evens = tuple(point['location'] for idx, point in enumerate(all_data[:-2])
                  if _is_even(idx))
    odds = tuple(point['location'] for idx, point in enumerate(all_data[2:])
                 if not _is_even(idx))
    return evens, odds

def _is_even(number: int) -> bool:
    return number % 2 == 0

def _average_value(data: tuple, selector: Selector) -> str:
    pertinent_values = [point[selector.data_type][selector.key]
                        for point in data]
    try:
        val = sum(float(point) for point in pertinent_values) / len(data)
    except ValueError:
        val = Counter(pertinent_values).most_common()[0][0]
    return f'{val}{selector.symbol}'