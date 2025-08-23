########################################################
#################  WEATHER  AND  TIDE  #################
########################################################
from concurrent.futures import ThreadPoolExecutor
import datetime
from functools import partial
from pathlib import Path

from weather_and_tide import (
    api_caller,
    config,
    email_generator,
    mailer,
    response_parser,
)

# Load configuration
STORMGLASS_API_KEY = config.STORMGLASS_API_KEY
user_config: config.Config = config.load_config(Path(
    config.PROJECT_ROOT / "config.yaml")
)

# Fetch weather warnings
warnings_response = api_caller.fetch_warnings()
if warnings_response:
    weather_warnings = response_parser.parse_warnings(warnings_response)
else:
    weather_warnings = []

# Fetch and parse forecasts on separate threads
with ThreadPoolExecutor() as executor:
    fetch_with_api_key = partial(api_caller.fetch_forecast, api_key=STORMGLASS_API_KEY)
    forecasts = executor.map(fetch_with_api_key, user_config.locations)
    fmt_rows = (response_parser.parse_forecast(forecast) for forecast in forecasts)

# Generate email
email_data: dict[str, list] = {
    "warnings": weather_warnings,
    "locations": [],
}
for location, row_data in zip(user_config.locations, fmt_rows):
    location_summary = {"name": location.name, "type": location.info, "rows": row_data}
    email_data["locations"].append(location_summary)

html_email: str = email_generator.generate_email(email_data)

# Send email
today_date_fmt = datetime.date.today().strftime("%d %B")
mailer.send_email(html_email, user_config.email_recipients, today_date_fmt)
