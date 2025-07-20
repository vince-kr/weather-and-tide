import datetime
from operator import attrgetter
from typing import Generator, Literal

from pydantic import BaseModel


class WeatherWarning(BaseModel):
    id: int
    level: Literal["Red", "Orange", "Yellow"]
    headline: str
    onset: datetime.datetime
    expiry: datetime.datetime
    description: str
    regions: list[str]

    @property
    def level_index(self) -> int:
        return ("Red", "Orange", "Yellow").index(self.level)

def generate_warnings(
        warnings_response: list[dict],
        desired_fips: list[str]
) -> list[WeatherWarning]:
    warning_objects = (WeatherWarning.model_validate(raw_warning)
                       for raw_warning in warnings_response)
    filtered_wgs = (wg for wg in warning_objects
                    if set(wg.regions) & set(desired_fips))
    sorted_county = _sort_by_county(filtered_wgs, desired_fips)
    sorted_level = sorted(sorted_county, key=attrgetter("level_index"))
    return sorted_level[:4]


def _sort_by_county(
        warnings: Generator[WeatherWarning, None, None],
        desired_fips: list[str]
) -> list[WeatherWarning]:
    county_order = {code: i for i, code in enumerate(desired_fips)}

    def sort_key(wg: WeatherWarning):
        valid_codes = (county_order[code] for code in wg.regions
                       if code in county_order)
        return min(valid_codes)

    return sorted(warnings, key=sort_key)
