import datetime
import json
import requests
from typing import Iterable

today = datetime.date.today()
TIDES_URL = 'https://api.stormglass.io/v2/tide/extremes/point'
START = today.isoformat()
END = (today + datetime.timedelta(hours=15)).isoformat()
type TideResponse = Iterable[dict[str, float, str, str, str, str]]

def request_tide_times(
        coords: tuple[float, float],
        api_key: str
) -> TideResponse | None:
    request_object = _generate_tide_request_object(coords, api_key)
    response = requests.get(**request_object)
    if response.ok:
        return _pertinent_content(response.content)

def _generate_tide_request_object(
        coords: tuple[float, float],
        api_key: str
) -> dict:
    lat, long = coords
    return {
        'url': TIDES_URL,
        'params': {
            'lat': lat,
            'lng': long,
            'start': START,
            'end': END
        },
        'headers': {
            'Authorization': api_key
        }
    }

def _pertinent_content(raw_response: bytes) -> TideResponse:
    return json.loads(raw_response)['data']