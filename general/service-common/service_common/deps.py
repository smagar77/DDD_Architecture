import inject
from fastapi import Depends

from service_common import constants
from service_common.schema import AuthenticationSchema
from service_common.utils import extract_authenticated_user
from service_common.repository import RedisRepository
from service_common.error import ApplicationError


async def get_authorised_user(token: str = Depends(AuthenticationSchema())):
    """

    :param token:
    :return:
    """

    public_id = extract_authenticated_user(token)
    repo = RedisRepository()
    token_data = repo.get(public_id)
    if token_data:
        return public_id
    raise ApplicationError(response_code=constants.HTTP_401_UNAUTHORIZED, message="User already logout.")
