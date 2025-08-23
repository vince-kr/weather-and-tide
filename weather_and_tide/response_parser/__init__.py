from weather_and_tide import config
from weather_and_tide.response_parser import (
    parse_tide,
    parse_warning,
    parse_weather
)

user_config: config.Config = config.load_config(config.PROJECT_ROOT / "example.config.yaml")

def parse_forecast(forecast: dict) -> zip | tuple:
    if "weatherdata" in forecast:
        return parse_weather.generate_weather_rows(forecast)
    else:
        return parse_tide.generate_tide_rows(forecast)

def parse_warnings(warnings_response: list[dict]) -> parse_warning.WeatherWarningsList:
    warning_objects = (parse_warning.WeatherWarning.model_validate(raw_warning)
                       for raw_warning in warnings_response)
    warnings_list = parse_warning.WeatherWarningsList(warning_objects, user_config.county_warnings)
    fs_warnings = warnings_list.filter_by_county().sort_by_county().sort_by_severity()
    return fs_warnings[:4]
