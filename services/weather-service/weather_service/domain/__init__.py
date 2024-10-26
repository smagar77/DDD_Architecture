import typing
import datetime
import decimal
from pydantic import Field
from service_common.domains import BaseDomain


class CachedData(BaseDomain):
    _protected_fields: list = []

    public_id: str = Field(default=0, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    modified_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    response: typing.Union[list, dict] = Field(default_factory=dict)


class CachedLocation(CachedData):
    _protected_fields: list = []

    latitude: decimal.Decimal = None
    longitude: decimal.Decimal = None

    class Config:
        orm_mode = True

    @property
    def location_key(self):
        if self.response:
            return self.response.get('Key')


class CachedForcast(CachedData):
    _protected_fields: list = []

    location_key: typing.Any = None
    type: str = None

    class Config:
        orm_mode = True
