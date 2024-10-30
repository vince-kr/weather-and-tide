########################################################
#################  WEATHER  AND  TIDE  #################
########################################################
import apis
import config_loader
import datetime
import email_generator
import mailer
from pathlib import Path
import response_parser

# Load configuration
API_KEY = config_loader.STORMGLASS_API_KEY
locations = config_loader.load_locations(Path('locations.yaml'))

# Collect data
formatted_forecasts = []
for location in locations:
    if location.info == 'weather':
        weather_response = apis.request_weather_forecast(location.coords)
        weather_rows = response_parser.generate_weather_rows(
            weather_response)
        formatted_forecasts.append(weather_rows)
    if location.info == 'tide':
        tide_response = apis.request_tide_times(location.coords, API_KEY)
        tide_rows = response_parser.generate_tide_rows(tide_response)
        formatted_forecasts.append(tide_rows)

# Generate email
email_data = { 'locations': [] }
for location, row_data in zip(locations, formatted_forecasts):
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
