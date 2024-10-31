########################################################
#################  WEATHER  AND  TIDE  #################
########################################################
import api_caller
import config_loader
import datetime
import email_generator
import mailer
from pathlib import Path
import response_parser

# Load configuration
API_KEY = config_loader.STORMGLASS_API_KEY
locations = config_loader.load_locations(Path('locations.yaml'))

# Fetch and format forecast data
forecasts = (api_caller.fetch_forecast(location, API_KEY) for location in locations)
fmt_rows = (response_parser.parse_forecast(forecast) for forecast in forecasts)

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
