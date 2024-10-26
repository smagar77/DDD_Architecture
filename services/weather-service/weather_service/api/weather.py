import json

from fastapi import Depends
from service_common.router import APIRouter
from service_common.schema import ResponseSchema

from weather_service.api import schema
from service_common.deps import get_authorised_user
from weather_service.service.weather import WeatherService

router = APIRouter(prefix='/weather', tags=['Weather Service'])


@router.get("/daily", response_model=schema.DailyForecastResponse)
async def get_daily_forecast(
        location: schema.LocationSchema = Depends(schema.LocationSchema),
        current_user: str = Depends(get_authorised_user)
):
    service = WeatherService()
    resp = service.get_daily_forecast(location.lat, location.long)
    if resp:
        return resp


@router.get("/hourly", response_model=schema.HourlyForecastResponse)
async def get_hourly_forecast(location: schema.LocationSchema = Depends(schema.LocationSchema),
                              current_user: str = Depends(get_authorised_user)):
    service = WeatherService()
    resp = service.get_hourly_forecast(location.lat, location.long)
    if resp:
        return {"HourlyForecasts": resp}
