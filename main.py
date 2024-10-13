################################################
#############  WEATHER  AND  TIDE  #############
################################################
from pathlib import Path

import config_loader

# Start by loading configuration
STORMGLASS_API_KEY = config_loader.STORMGLASS_API_KEY
locations = config_loader.load_locations(Path('locations.yaml'))

# Collect some data
# tide_times = apis.request_tide_times()
