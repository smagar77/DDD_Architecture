import typing
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from service_common.schema import BaseRequestSchema


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def transform_to_utc_datetime(dt: datetime) -> datetime:
    return dt.astimezone(tz=timezone.utc)


class LocationSchema(BaseRequestSchema):
    lat: float
    long: float


class HeadlineSchema(BaseModel):
    EffectiveDate: datetime = None
    EffectiveEpochDate: int = None
    Severity: int = None
    Text: str = None
    Category: str = None
    EndDate: datetime = None
    EndEpochDate: int = None
    MobileLink: str = None
    Link: str = None


class TemperatureSchema(BaseModel):
    Value: float = None
    Unit: str = None
    UnitType: int = None


class TemperatureForecastSchema(BaseModel):
    Minimum: TemperatureSchema = Field(default_factory=TemperatureSchema)
    Maximum: TemperatureSchema = Field(default_factory=TemperatureSchema)


class Forecast(BaseModel):
    Icon: int = None
    IconPhrase: str = None
    HasPrecipitation: bool = None


class DailyForecastSchema(BaseModel):
    Date: datetime = None
    EpochDate: int = None
    Temperature: TemperatureForecastSchema = Field(default_factory=TemperatureForecastSchema)
    Day: Forecast = None
    Night: Forecast = None
    Sources: typing.List[str] = Field(default_factory=list)
    MobileLink: str = None
    Link: str = None


class DailyForecastResponse(BaseModel):
    Headline: HeadlineSchema = Field(default_factory=HeadlineSchema)
    DailyForecasts: typing.List[DailyForecastSchema] = Field(default_factory=list)


class HourlyForecast(BaseModel):
    DateTime: datetime = None
    EpochDateTime: int = None
    WeatherIcon: int = None
    IconPhrase: str = None
    HasPrecipitation: bool = None
    IsDaylight: bool = None
    Temperature: TemperatureSchema = Field(default_factory=TemperatureSchema)
    PrecipitationProbability: float = None
    MobileLink: str = None
    Link: str = None


class HourlyForecastResponse(BaseModel):
    HourlyForecasts: typing.List[HourlyForecast] = Field(default_factory=list)


"""
https://dataservice.accuweather.com/forecasts/v1/daily/5day/204848?apikey=jCLPUDFqHDZV7369qCF3gfHGutmpcVKG
http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/204848?apikey=jCLPUDFqHDZV7369qCF3gfHGutmpcVKG
"""