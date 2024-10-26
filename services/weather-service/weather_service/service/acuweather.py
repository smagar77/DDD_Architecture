import inject
import requests
import urllib
from service_common.settings import CoreSettings


class AcuWeatherService:
    base_url: str = "http://dataservice.accuweather.com"
    api_key: str = None

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_location_key(self, lat, long):
        endpoint = "locations/v1/cities/geoposition/search"
        params = {
            "apikey": self.api_key,
            "q": f"{lat},{long}",
            "language": "en-us",
            "details": "false",
            "toplevel": "false"
        }
        params = urllib.parse.urlencode(params)
        url = f"{self.base_url}/{endpoint}?{params}"
        resp = requests.get(url)
        data = resp.json()
        return data

    def get_daily_forecast(self, loc_key):
        endpoint = "forecasts/v1/daily/5day"
        params = {
            "apikey": self.api_key,
            "language": "en-us",
            "details": "True",
            "metric": "True"
        }
        params = urllib.parse.urlencode(params)
        url = f"{self.base_url}/{endpoint}/{loc_key}?{params}"
        resp = requests.get(url)
        data = resp.json()
        return data

    def get_hourly_forecast(self, loc_key):
        endpoint = "forecasts/v1/hourly/12hour"
        params = {
            "apikey": self.api_key,
            "language": "en-us",
            "details": "True",
            "metric": "True"
        }
        params = urllib.parse.urlencode(params)
        url = f"{self.base_url}/{endpoint}/{loc_key}?{params}"
        resp = requests.get(url)
        data = resp.json()
        return data
