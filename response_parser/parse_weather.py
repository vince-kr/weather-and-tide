from collections import Counter, namedtuple
import datetime
import itertools
from typing import Any, Generator, Iterable, Sequence, TypeVar

from pydantic import BaseModel, Field

Selector = namedtuple(
    "Selector", "data_type key symbol"
)

weather_selectors = (
    Selector("temperature", "value", "° C",),
    Selector("precipitation", "value", " mm"),
    Selector("wind_speed", "mps", " km/h"),
    Selector("wind_direction", "name", ""),
    Selector("cloudiness", "percent", "%"),
)

weather_row_headers = (
    "",
    "Temperature",
    "Precipitation",
    "Wind speed",
    "Wind direction",
    "Cloud cover",
)

T = TypeVar('T')

class Temperature(BaseModel):
    unit: str = Field(alias="@unit")
    value: float = Field(alias="@value")


class WindDirection(BaseModel):
    name: str = Field(alias="@name")


class WindSpeed(BaseModel):
    mps: float = Field(alias="@mps")
    beaufort: float = Field(alias="@beaufort")


class Cloudiness(BaseModel):
    percent: float = Field(alias="@percent")


class Precipitation(BaseModel):
    unit: str = Field(alias="@unit")
    value: float = Field(alias="@value")


class LocationForPoint(BaseModel):
    temperature: Temperature
    windDirection: WindDirection
    windSpeed: WindSpeed
    cloudiness: Cloudiness


class LocationForPeriod(BaseModel):
    precipitation: Precipitation


class ForecastForPoint(BaseModel):
    location: LocationForPoint


class ForecastForPeriod(BaseModel):
    location: LocationForPeriod


class ForecastHour:
    """Represents one hour of forecast including both point and period data."""
    def __init__(self, forecast: tuple[ForecastForPoint, ForecastForPeriod]):
        point, period = forecast
        self.temperature: Temperature = point.location.temperature
        self.wind_direction: WindDirection = point.location.windDirection
        self.wind_speed: WindSpeed = point.location.windSpeed
        self.cloudiness: Cloudiness = point.location.cloudiness
        self.precipitation: Precipitation = period.location.precipitation


class ForecastBatch:
    """Represents three hours of forecast data."""
    def __init__(self, batch: tuple[ForecastHour, ...]):
        self._batch = batch

    @staticmethod
    def _average(values: Sequence[T]) -> T:
        return sum(values) / len(values)

    @property
    def temperature(self) -> Temperature:
        """Average temperature over the three hours."""
        average = self._average(tuple(hour.temperature.value for hour in self._batch))
        return Temperature.model_validate(
            {
            "@unit": self._batch[0].temperature.unit,
            "@value": average
            }
        )

    @property
    def wind_speed(self) -> WindSpeed:
        """Average wind speed over the three hours."""
        average_mps = self._average(tuple(hour.wind_speed.mps for hour in self._batch))
        average_kph = average_mps * 3.6
        average_bft = self._average(tuple(hour.wind_speed.beaufort for hour in self._batch))
        return WindSpeed.model_validate(
            {
                "@mps": average_kph,
                "@beaufort": average_bft
            }
        )

    @property
    def wind_direction(self) -> WindDirection:
        """Most common wind direction over the three hours."""
        directions = [hour.wind_direction.name for hour in self._batch]
        most_common = Counter(directions).most_common(1)[0][0]
        return WindDirection.model_validate({"@name": most_common})

    @property
    def cloudiness(self) -> Cloudiness:
        """Average cloudiness over the three hours."""
        average_percent = self._average(tuple(hour.cloudiness.percent for hour in self._batch))
        return Cloudiness.model_validate({"@percent": average_percent})

    @property
    def precipitation(self) -> Precipitation:
        """Average precipitation over the three hours."""
        average_precip = self._average(tuple(
            hour.precipitation.value for hour in self._batch))
        unit = self._batch[0].precipitation.unit
        return Precipitation.model_validate({"@unit": unit, "@value": average_precip})

def generate_weather_rows(weather: dict) -> zip:
    forecasts = weather["weatherdata"]["product"]["time"]
    point_in_time, period_of_time = _split_by_index(forecasts[:26])
    point_in_time_forecasts = tuple(
        ForecastForPoint.model_validate(point) for point in point_in_time
    )
    period_of_time_forecasts = tuple(
        ForecastForPeriod.model_validate(period) for period in period_of_time
    )
    forecast_hours: Iterable[ForecastHour] = (
        ForecastHour(pair)
        for pair in zip(point_in_time_forecasts, period_of_time_forecasts)
    )
    forecast_batches: Iterable[ForecastBatch] = tuple(
        ForecastBatch(three_hours) for three_hours in _batched(forecast_hours, 3))
    hours = _calculate_hours(datetime.datetime.now())
    average_values = []
    for selector in weather_selectors:
        values = []
        for batch in forecast_batches:
            required_object = getattr(batch, selector.data_type)
            required_value = getattr(required_object, selector.key)
            try:
                fmt_value = f"{required_value:.1f}{selector.symbol}"
            except ValueError:
                fmt_value = required_value
            values.append(fmt_value)
        average_values.append(tuple(values))
    rows = tuple([hours, *tuple(average_values)])
    return zip(weather_row_headers, tuple(rows))


def _split_by_index(all_data: Sequence) -> tuple:
    """Given an iterable, return a 2-tuple of tuples that contain:
    - all even indices from the iterable minus the last one
    - all odd indices from the iterable minus the first one
    """
    even_without_last = tuple(
        point for idx, point in enumerate(all_data[:-2]) if idx % 2 == 0
    )
    odd_without_first = tuple(
        point for idx, point in enumerate(all_data[2:]) if idx % 2 != 0
    )
    return even_without_last, odd_without_first


def _calculate_hours(current_time: datetime.datetime) -> tuple[str, ...]:
    datetime_objects = ((current_time + datetime.timedelta(hours=i))
                         for i in (0, 3, 6, 9, 12))
    hours_fmt = tuple(f"{start.hour}:00 - {stop.hour}:00"
                 for start, stop in itertools.pairwise(datetime_objects))
    return hours_fmt


def _batched(data: Iterable[T], length: int) -> Generator[tuple[T, ...], Any, None]:
    iterator = iter(data)
    while batch := tuple(itertools.islice(iterator, length)):
        yield batch

