from collections import UserList
import datetime
from operator import attrgetter
from typing import Iterable, Literal

from pydantic import BaseModel

from weather_and_tide import config

user_config = config.load_config(config.PROJECT_ROOT / "example.config.yaml")
desired_fips = user_config.county_warnings

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

    @property
    def text_description(self):
        return self.description.split(" •")[0]

    @property
    def impacts(self):
        return self.description.split(" •")[1:]

class WeatherWarningsList(UserList[WeatherWarning]):
    def __init__( self,
                  warnings: Iterable[WeatherWarning],
                  fips_list: list[str] | None = None) -> None:
        super().__init__(warnings)
        if fips_list:
            self.fips_list = fips_list
        else:
            self.fips_list = desired_fips

    def filter_by_county(self) -> "WeatherWarningsList":
        return WeatherWarningsList(
            [wg for wg in self
             if set(wg.regions) & set(self.fips_list)],
            self.fips_list,
        )

    def sort_by_severity(self) -> "WeatherWarningsList":
        warnings_by_severity = sorted(self, key=attrgetter("level_index"))
        return WeatherWarningsList(warnings_by_severity, self.fips_list)

    def sort_by_county(self) -> "WeatherWarningsList":
        county_order = {code: i for i, code in enumerate(self.fips_list)}

        def sort_key(wg: WeatherWarning):
            valid_codes = (county_order[code] for code in wg.regions
                           if code in county_order)
            return min(valid_codes)

        return WeatherWarningsList(sorted(self, key=sort_key), self.fips_list)
