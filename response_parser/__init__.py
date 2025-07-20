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

def parse_warnings(warnings: list[dict], desired_counties: list[str]) -> list:
    return parse_warning.generate_warnings(warnings, desired_counties)

def format_moon_phase(moon_phase: dict) -> str:
    return parse_moon_phase.format_moon_phase(moon_phase)