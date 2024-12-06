# Weather and tide

## What is it?

Gather local weather and tide forecasts for configurable locations and send them via email.

## Dependencies

Ensure that the `python` command is recognised by your path, and points to a Python version 3.12 or higher.

All package dependencies will be resolved automatically (inside a venv) by the run script.

## Installation

### Clone the git repo and change to the directory

```bash
git clone https://github.com/vince-kr/weather-and-tide && cd weather-and-tide
```

### Create locations.yaml and .env files

Examples and suggestions for each can be found in `example.locations.yaml` and `example.env` respectively.

### Execute `run.py`

This will

1. Check that a local virtual environment exists; if not, create it
2. Check that required dependencies are installed; if not, install them
3. Fetch forecasts as defined in `locations.yaml` and send them by email

In other words; the first time that the project is run, it will create a virtual environment and install dependencies before running the main flow. Every subsequent run will confirm that the venv and dependencies are already in place and will only execute the main flow.

If you prefer more control, you can create your own virtual environment to install dependencies then execute `main.py` with the environment Python.

### (Optional) Schedule execution

For example using crontab: run `crontab -e` and add the line `0 6 * * * 
/path/to/weahter-and-tide/venv/bin/python /path/to/weather-and-tide/run.py` to execute the 
script every morning at 
6am system time.

## Contributing

I'm very happy to accept pull requests for improvements or new features. Once you build a local venv and install dependencies (whether using the run script or manually) all developer tests should be passing. Integration tests require a valid API key as well as a working sender email address + password to succeed.

Please follow the usual branch-contrib-push-pr flow, ensuring that all developer tests are passing before you raise the PR.
