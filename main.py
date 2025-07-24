########################################################
#################  WEATHER  AND  TIDE  #################
########################################################
from concurrent.futures import ThreadPoolExecutor
import datetime
import json
from functools import partial
from pathlib import Path

import api_caller
import config
import email_generator
import mailer
import response_parser

# Load configuration
APIVERVE_API_KEY = config.APIVERVE_API_KEY
STORMGLASS_API_KEY = config.STORMGLASS_API_KEY
user_config: config.Config = config.load_config(Path(config.PROJECT_ROOT / "config.yaml"))

# Fetch weather warnings
with open(config.PROJECT_ROOT / "county_to_fips.json") as cf:
    counties_to_fips: dict[str, str] = json.load(cf)
desired_counties: list[str] = [counties_to_fips[name]
                               for name in user_config.county_warnings]
warnings_response = api_caller.fetch_warnings()
weather_warnings = response_parser.parse_warnings(warnings_response, desired_counties)

# Fetch the current phase of the moon
# moon_phase = api_caller.fetch_moon_phase(APIVERVE_API_KEY)
moon_phase = {}
if moon_phase:
    moon_phase_fmt = response_parser.format_moon_phase(moon_phase)
else:
    moon_phase_fmt = "Unknown"

# Fetch and parse forecasts on separate threads
with ThreadPoolExecutor() as executor:
    fetch_with_api_key = partial(api_caller.fetch_forecast, api_key=STORMGLASS_API_KEY)
    forecasts = executor.map(fetch_with_api_key, user_config.locations)
    fmt_rows = (response_parser.parse_forecast(forecast) for forecast in forecasts)

# Generate email
email_data: dict[str, list] = {
    "warnings": weather_warnings,
    "moon_phase": moon_phase_fmt,
    "locations": [],
}
for location, row_data in zip(user_config.locations, fmt_rows):
    location_summary = {"name": location.name, "type": location.info, "rows": row_data}
    email_data["locations"].append(location_summary)

html_email: str = email_generator.generate_email(email_data)

# Send email
today_date_fmt = datetime.date.today().strftime("%d %B")
mailer.send_email(html_email, user_config.email_recipients, today_date_fmt)
