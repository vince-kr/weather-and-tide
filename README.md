# Weather and tide

## What is it?

Gather local weather and tide forecasts for configurable locations and send them via email.

## Installation

### Clone the git repo and change to the directory

```bash
git clone https://github.com/vince-kr/weather-and-tide && cd weather-and-tide
```

### Create locations.yaml and .env files

Examples and suggestions for each can be found in `locations.yaml.example` and `.env.example` respectively.

### Execute `run.py`

This will

1. Check that a local virtual environment exists; if not, create it
2. Check that required dependencies are installed; if not, install them
3. Fetch forecasts as defined in `locations.yaml` and send them by email

### (Optional) Schedule execution

For example using crontab: run `crontab -e` and add the line `0 6 * * * /path/to/weather-and-tide/run.py` to execute the script every morning at 6am system time.
