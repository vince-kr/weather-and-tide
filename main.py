########################################################
#################  WEATHER  AND  TIDE  #################
########################################################
import apis
import config_loader
import mailer
from pathlib import Path
import response_formatter
import templater

# Start by loading configuration
STORMGLASS_API_KEY = config_loader.STORMGLASS_API_KEY
locations = config_loader.load_locations(Path('locations.yaml'))

# Collect some data
location = locations[0]
tide_response = apis.request_tide_times(location.coords, STORMGLASS_API_KEY)

# Format the response
tide_times: dict = response_formatter.generate_tide_times(tide_response)

# Generate email
html_email: str = templater.generate_email(tide_times)

# Send email
mailer.send_email(html_email)