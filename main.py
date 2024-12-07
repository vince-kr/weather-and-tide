########################################################
#################  WEATHER  AND  TIDE  #################
########################################################
from functools import partial

import api_caller
from concurrent.futures import ThreadPoolExecutor
import config
import datetime
import email_generator
import mailer
from pathlib import Path
import response_parser

# Load configuration
APIVERVE_API_KEY = config.APIVERVE_API_KEY
STORMGLASS_API_KEY = config.STORMGLASS_API_KEY
user_config = config.load_config(Path(config.PROJECT_ROOT / "config.yaml"))

# Fetch the current phase of the moon
moon_phase = api_caller.fetch_moon_phase(APIVERVE_API_KEY)
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
