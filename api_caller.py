from datetime import date, timedelta
import requests
import xmltodict

from config import Location  # TODO

MOON_URL = "https://api.apiverve.com/v1/moonphases?today=true"
TIDES_URL = 'https://api.stormglass.io/v2/tide/extremes/point'
WEATHER_URL = 'http://openaccess.pf.api.met.ie/metno-wdb2ts/locationforecast'
WEATHER_WARNING_URL = "https://www.met.ie/Open_Data/json/warning_IRELAND.json"

def fetch_moon_phase(api_key: str) -> dict | None:
    request_object = {
        'url': MOON_URL,
        'headers': {
            'x-api-key': api_key
        }
    }
    response = requests.get(**request_object)
    if response.ok:
        return response.json()["data"]
    return None

def fetch_warnings() -> list[dict] | None:
    request_object = {
        'url': WEATHER_WARNING_URL
    }
    response = requests.get(**request_object)
    if response.ok:
        return response.json()
    return None

def fetch_forecast(location: Location, api_key: str) -> dict | None:
    match location.info:
        case 'weather':
            result = _fetch_weather_forecast(location.coords)
        case 'tide':
            result = _fetch_tide_forecast(location.coords, api_key)
        case _:
            result = None
    return result

def _build_weather_request(url: str, coords: tuple[float, float]):
    lat, long = coords
    return {
        'url': url + f'?lat={lat};long={long}'
    }

def _build_tide_request(
        url: str,
        coords: tuple[float, float],
        api_key: str
) -> dict:
    lat, long = coords
    start = date.today().isoformat() + 'T00:00:00'
    end = (date.today() + timedelta(days=1)).isoformat() + 'T00:00:00'
    return {
        'url': url,
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

def _fetch_weather_forecast(coords: tuple[float, float]) -> dict | None:
    request_object = _build_weather_request(WEATHER_URL, coords)
    response = requests.get(**request_object)
    if response.ok:
        return xmltodict.parse(response.content)
    return None

def _fetch_tide_forecast(
        coords: tuple[float, float],
        api_key: str
) -> dict | None:
    request_object = _build_tide_request(TIDES_URL, coords, api_key)
    response = requests.get(**request_object)
    if response.ok:
        return response.json()
    return None
