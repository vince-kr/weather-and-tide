import datetime
from jinja2 import Template

with open("weather-tide-template.html") as wtt:
    template = Template(wtt.read())

weather_row_headers = (
    "Temperature",
    "Precipitation",
    "Wind speed",
    "Wind direction",
    "Cloud cover",
)

weather_row_contents = (
    (
        "9.1° C",
        "9.2° C",
        "8.3° C",
        "7.5° C",
    ),
    (
        "0 mm",
        "0.7 mm",
        "1.7 mm",
        "2.2 mm",
    ),
    (
        "24.6 km/h",
        "25.2 km/h",
        "31.1 km/h",
        "36.2 km/h",
    ),
    (
        "N",
        "N",
        "N",
        "N",
    ),
    (
        "98.5%",
        "100.0",
        "100.0",
        "100.0",
    ),
)

tide_rows = (
    (
        "Low",
        ("18:31",),
    ),
    (
        "High",
        ("00:49",),
    ),
    (
        "Low",
        ("07:07",),
    ),
)

data = {
    "today": datetime.date.today().strftime("%d %B"),
    "locations": [
        {
            "name": "Bray Head",
            "type": "weather",
            "rows": zip(weather_row_headers, weather_row_contents)
        },
        {
            "name": "Bray seafront",
            "type": "tide",
            "rows": tide_rows
        },
    ]
}

html_email = template.render(data)
with open("weather-tide-email.html", "w") as wte:
    wte.write(html_email)
