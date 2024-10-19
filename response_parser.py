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
import apis


def format_tide_response(tides: dict) -> tuple:
    rows = tuple(
        (
            tide_datum['type'].capitalize(),
            tuple((_extract_time_from(tide_datum['time']),))
        )
        for tide_datum in tides['data']
    )
    return rows

def _extract_time_from(datetimestamp: str) -> str:
    return datetimestamp[11:16]