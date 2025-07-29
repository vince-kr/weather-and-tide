
from response_parser import (
    parse_moon_phase,
    parse_tide,
    parse_warning,
    parse_weather
)


def parse_forecast(forecast: dict) -> zip | tuple:
    if "weatherdata" in forecast:
        return parse_weather.generate_weather_rows(forecast)
    else:
        return parse_tide.generate_tide_rows(forecast)

def parse_warnings(warnings_response: list[dict]) -> parse_warning.WeatherWarningsList:
    warning_objects = (parse_warning.WeatherWarning.model_validate(raw_warning)
                       for raw_warning in warnings_response)
    warnings_list = parse_warning.WeatherWarningsList(warning_objects)
    fs_warnings = warnings_list.filter_by_county().sort_by_county().sort_by_severity()
    return fs_warnings[:4]

def format_moon_phase(moon_phase: dict) -> str:
    return parse_moon_phase.format_moon_phase(moon_phase)