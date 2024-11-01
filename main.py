########################################################
#################  WEATHER  AND  TIDE  #################
########################################################
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
    forecast_futures = [executor.submit(api_caller.fetch_forecast, location, API_KEY)
                        for location in locations]
    fmt_rows = [response_parser.parse_forecast(fc_future.result())
                for fc_future in forecast_futures]

# Generate email
email_data = { 'locations': [] }
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
