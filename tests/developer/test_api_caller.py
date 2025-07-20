import datetime

import pytest

import api_caller

@pytest.fixture
def dates():
    date_today = datetime.date.today()
    date_tomorrow = date_today + datetime.timedelta(days=1)
    return {
        "start_of_today": date_today.isoformat() + 'T00:00:00',
        "start_of_tomorrow": date_tomorrow.isoformat() + 'T00:00:00'
    }

@pytest.fixture
def coords():
    return 53.2048, -6.0979

def test_generate_weather_request_object(coords):
    base_url = 'http://some-fake-url.com/weather'
    expected = {
        'url': base_url + f'?lat=53.2048;long=-6.0979'
    }
    actual = api_caller._build_weather_request(base_url, coords)
    assert expected == actual

def test_generate_tide_request_object(dates, coords):
    base_url = 'http://some-fake-url.com/tides'
    lat, long = coords
    api_key = 'not-really-an-api-key'
    expected = {
        'url': base_url,
        'params': {
            'lat': lat,
            'lng': long,
            'start': dates['start_of_today'],
            'end': dates['start_of_tomorrow']
        },
        'headers': {
            'Authorization': api_key
        }
    }
    actual = api_caller._build_tide_request(base_url, (lat, long), api_key)
    assert expected == actual
