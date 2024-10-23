########################################################
#################  WEATHER  AND  TIDE  #################
########################################################
import apis
import config_loader
import datetime
import email_generator
from pathlib import Path
import response_parser

# Start by loading configuration
STORMGLASS_API_KEY = config_loader.STORMGLASS_API_KEY
locations = config_loader.load_locations(Path('locations.yaml'))

# Collect some data
location = locations[0]
weather_response = apis.request_weather_forecast(location.coords)
tide_response = apis.request_tide_times(location.coords, STORMGLASS_API_KEY)

# Format the response
weather_row_headers, weather_row_contents = response_parser.generate_weather_rows(
    weather_response)
tide_rows: tuple = response_parser.generate_tide_rows(tide_response)

# Generate email
email_data = {
    "today": datetime.date.today().strftime("%d %B"),
    "locations": [
        {
            "name": locations[0].name,
            "type": locations[0].info,
            "rows": tide_rows
        },
        {
            "name": locations[1].name,
            "type": locations[1].info,
            "rows": zip(weather_row_headers, weather_row_contents)
        },
    ]
}
html_email: str = email_generator.generate_email(email_data)

with open("wauw.html", "w") as em:
    em.write(html_email)

# Send email
# mailer.send_email(html_email)