import typing
import inject

from pymongo import MongoClient


class WeatherCacheRepository:
    forecast = None
    location = None

    @inject.autoparams('client')
    def __init__(self, client: MongoClient):
        self.is_enabled = False
        if client:
            self.is_enabled = True
            self.forecast = client.weather.forecast
            self.location = client.weather.location

    def cache_location(self, data: dict):
        if not self.is_enabled:
            return None
        result = self.location.indert_one(
            data
        )
        """
        result = self.location.update_one(
            {'latitude': data.get('latitude'),
             'longitude': data.get('longitude')},
            data,
            upsert=True
        )
        """
        return result

    def cache_forecast(self, data: dict):
        if not self.is_enabled:
            return None
        result = self.forecast.indert_one(
            data
        )
        """
        self.forecast.update_one(
            {'location_key': data.get('location_key'), 'type': data.get('type')},
            data,
            upsert=True
        )
        """
        return result

    def find_location(self, lat, long):
        if not self.is_enabled:
            return None
        result = self.location.find_one({'latitude': lat, 'longitude': long})
        if type(result) is list:
            result = result.pop(0)
        # Validate if cached record in valid
        return result

    def find_forecast(self, loc_key, type_):
        if not self.is_enabled:
            return None
        result = self.forecast.find_one(
            {'location_key': loc_key, 'type': type_}
        )
        if type(result) is list:
            result = result.pop(0)
        # Validate if cached record in valid
        return result
