from response_parser.parse_tide import (
    _extract_time_from,
    _generate_tide_rows,
)

from response_parser.parse_weather import (
    _extract_weather_datums,
    _combine_datums,
    _calculate_hours,
    Selector,
    _average_value,
    _avg_and_format,
    _generate_weather_rows
)

from response_parser.parse_warning import parse_warnings

def parse_forecast(forecast: dict) -> zip | tuple:
    if "weatherdata" in forecast:
        return _generate_weather_rows(forecast)
    else:
        return _generate_tide_rows(forecast)

