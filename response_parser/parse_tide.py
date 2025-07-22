import datetime
from typing import Literal

from pydantic import BaseModel, Field

class TideForecast(BaseModel):
    tide_time: datetime.datetime = Field(alias="time")
    tide_type: Literal["low", "high"] = Field(alias="type")

    @property
    def fmt_time(self):
        return self.tide_time.astimezone(tz=None).strftime("%H:%M")

    @property
    def fmt_type(self):
        return self.tide_type.capitalize()

def generate_tide_rows(tides: dict) -> tuple:
    tide_objects = [TideForecast.model_validate(tide) for tide in tides["data"]]
    return tuple(
        (
            tide_datum.fmt_type,
            tuple([tide_datum.fmt_time])
        )
        for tide_datum in tide_objects
    )
