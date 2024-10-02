# Weather and tide

A small app to grab data on weather and tide times from public APIs every morning, summarise them,
and send them from-to my own email address.

## Requirements

Send an email before 7am every morning with the weather forecast for that day at my location. The forecast should cover fourteen hours from 7am to 9pm and should contain at least the following information for each hour:

- Temperature
- Precipitation
- Wind speed
- Wind direction

The same email should also advise the high and low tide times at my favourite beach for that day.

## Notes on implementation of requirements

### Before 7am every morning

I can set up a cronjob on the home server to trigger a script every morning at 6:30. The script should take care of all component parts of the requirements:

- Get data on weather forecast and tide times
- Generate an email with a summary of this data
- Send the email

### Get weather forecast and tide times

I can use two separate APIs for this purpose. Weather information for any pair of latitude + longtitude coordinates can be obtained from met.ie's public API. Tide times can be obtained from stormglass.io where the free account allows up to ten calls per day.

### Summarise the data

I can use a dataclass or NamedTuple to turn the forecast data and tide times from the raw API response into easy to use objects. From there, using a HTML template (jinja2?) and dynamically adding tables for the data should be straightforward.

### Send the email

For now I will use my Greenhost account as the sender and receiver of the email. Python has good email libraries.

## General notes on implementation

### TDD

I will want to use TDD (with `unittest`) for summarising the data. Calling APIs and sending emails is not as easy (or as useful) to test.

### Configuration

The app requires some static data to do its job: the stormglass.io API key, coordinates of the locations to get data for, and email credentials. All of these represent private information that I would not want to include in a GitHub repo.
