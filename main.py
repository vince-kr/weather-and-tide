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
API_KEY = config.STORMGLASS_API_KEY
locations = config.load_locations(Path('locations.yaml'))

# Fetch and parse forecasts on separate threads
with ThreadPoolExecutor() as executor:
    fetch_with_api_key = partial(api_caller.fetch_forecast, api_key=STORMGLASS_API_KEY)
    forecasts = executor.map(fetch_with_api_key, locations)
    fmt_rows = (response_parser.parse_forecast(forecast) for forecast in forecasts)

# Generate email
email_data: dict[str, list] = { 'locations': [] }
for location, row_data in zip(locations, fmt_rows):
    location_summary = {
        'name': location.name,
        'type': location.info,
        'rows': row_data
    }
    email_data['locations'].append(location_summary)

html_email: str = email_generator.generate_email(email_data)

# Send email
today_date_fmt = datetime.date.today().strftime('%d %B')
mailer.send_email(html_email, today_date_fmt)
