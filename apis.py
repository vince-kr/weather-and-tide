import arrow
import requests
import xmltodict

TIDES_URL = 'https://api.stormglass.io/v2/tide/extremes/point'
WEATHER_URL = "http://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast"

def request_weather_forecast(coords: tuple[float, float]):
    lat, long = coords
    url = WEATHER_URL + f"?lat={lat};long={long}"
    response = requests.get(url)
    if response.ok:
        return xmltodict.parse(response.content)

def request_tide_times(
        coords: tuple[float, float],
        api_key: str
) -> dict | None:
    request_object = _generate_tide_request_object(coords, api_key)
    response = requests.get(**request_object)
    if response.ok:
        return response.json()

def _generate_tide_request_object(
        coords: tuple[float, float],
        api_key: str
) -> dict:
    lat, long = coords
    start = arrow.now().floor('day')
    end = arrow.now().shift(days=1).floor('day')
    return {
        'url': TIDES_URL,
        'params': {
            'lat': lat,
            'lng': long,
            'start': start,
            'end': end
        },
        'headers': {
            'Authorization': api_key
        }
    }