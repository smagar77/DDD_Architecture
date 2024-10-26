import typing

import inject

from service_common.repository import RedisRepository
from service_common.settings import CoreSettings


class TokenRedisRepository(RedisRepository):

    def __init__(self, *args, **kwargs):
        settings = inject.instance(CoreSettings)
        self.token_time_exp = settings.access_token_expire_minutes * 60
        super(TokenRedisRepository, self).__init__(*args, **kwargs)

    def add_token(self, uuid, token_data):
        self._add(uuid, token_data, ex=self.token_time_exp)

    def get_token(self, uuid) -> typing.Optional[dict]:
        return self.backend.get_dict(uuid)

    def delete(self, uuid):
        self.backend.delete(uuid)
