import inject
from weather_service.service.acuweather import AcuWeatherService
from weather_service.service.unit_of_work import UnitOfWork
from weather_service import domain


class WeatherService:
    backend: AcuWeatherService = None

    @inject.autoparams('uow', 'backend')
    def __init__(self, uow: UnitOfWork, backend: AcuWeatherService):
        self.uow = uow
        self.backend = backend

    def find_location_key(self, lat, lon):
        with self.uow:
            key_ = None
            data = self.uow.cache.find_location(lat, lon)
            if data:
                data = domain.CachedLocation.from_orm(data)
                key_ = data.location_key
            if not key_:
                # No valid cache record found so calling API
                resp = self.backend.get_location_key(lat, lon)
                if resp:
                    data = domain.CachedLocation(
                        **{
                            'latitude': lat,
                            'longitude': lon,
                            'response': resp
                        }
                    )
                    key_ = data.location_key
                    self.uow.cache.cache_location(data.dict())
            return key_

    def get_daily_forecast(self, lat, lon):
        key_ = self.find_location_key(lat, lon)
        if key_:
            with self.uow:
                data = self.uow.cache.find_forecast(key_, 'DAILY')
                if data:
                    data = domain.CachedForcast.from_orm(data)
                if not data:
                    resp = self.backend.get_daily_forecast(key_)
                    if resp:
                        data = domain.CachedForcast(**{
                            'location_key': key_,
                            'type': 'DAILY',
                            'response': resp
                        })
                        self.uow.cache.cache_forecast(data.dict())
                if data:
                    return data.response

    def get_hourly_forecast(self, lat, lon):
        key_ = self.find_location_key(lat, lon)
        if key_:
            with self.uow:
                data = self.uow.cache.find_forecast(key_, 'HOURLY')
                if data:
                    data = domain.CachedForcast.from_orm(data)
                if not data:
                    resp = self.backend.get_hourly_forecast(key_)
                    if resp:
                        data = domain.CachedForcast(**{
                            'location_key': key_,
                            'type': 'HOURLY',
                            'response': resp
                        })
                        self.uow.cache.cache_forecast(data.dict())
                if data:
                    return data.response
