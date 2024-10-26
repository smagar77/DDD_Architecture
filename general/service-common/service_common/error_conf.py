"""
Error Configuration file to map error codes with messages
"""
from service_common import constants
from service_common.enums import ResponseTypeEnum
from service_common.singlton_meta import SingletonMeta


class ErrorConfig(metaclass=SingletonMeta):
    """
    Keeps the error/Success messages at one place
    """
    _error_config: dict = {}

    def __init__(self):
        pass

    @classmethod
    def extend(cls, conf: dict):
        cls._error_config.update(conf)

    @classmethod
    def get(cls, code: int):
        return cls._error_config.get(code, {}).copy()


# Internal application messages
ErrorConfig.extend({
    constants.HTTP_500_INTERNAL_SERVER_ERROR: {
        'response_code': constants.HTTP_500_INTERNAL_SERVER_ERROR,
        'http_code': constants.HTTP_500_INTERNAL_SERVER_ERROR,
        'response_type': ResponseTypeEnum.error,
        'message': 'Internal server error. Please contact site administrator.',
    },
    constants.HTTP_401_UNAUTHORIZED: {
        'response_code': constants.HTTP_401_UNAUTHORIZED,
        'http_code': constants.HTTP_401_UNAUTHORIZED,
        'response_type': ResponseTypeEnum.error,
        'message': 'User token expired',
    },
    constants.HTTP_429_TOO_MANY_REQUESTS: {
        'response_code': constants.HTTP_429_TOO_MANY_REQUESTS,
        'http_code': constants.HTTP_429_TOO_MANY_REQUESTS,
        'response_type': ResponseTypeEnum.error,
        'message': 'Request limit reached.',
    },
    constants.HTTP_404_NOT_FOUND: {
        'response_code': constants.HTTP_404_NOT_FOUND,
        'http_code': constants.HTTP_404_NOT_FOUND,
        'response_type': ResponseTypeEnum.error,
        'message': 'Record not found',
    },
    constants.HTTP_417_EXPECTATION_FAILED: {
        'response_code': constants.HTTP_417_EXPECTATION_FAILED,
        'http_code': constants.HTTP_417_EXPECTATION_FAILED,
        'response_type': ResponseTypeEnum.error,
        'message': 'System is not in a state to perform this operation',
    },
    constants.HTTP_422_UNPROCESSABLE_ENTITY: {
        'response_code': constants.HTTP_422_UNPROCESSABLE_ENTITY,
        'http_code': constants.HTTP_422_UNPROCESSABLE_ENTITY,
        'response_type': ResponseTypeEnum.error,
        'message': 'Some data is missing',
    },
    constants.HTTP_201_CREATED: {
        'response_code': constants.HTTP_201_CREATED,
        'http_code': constants.HTTP_201_CREATED,
        'response_type': ResponseTypeEnum.success,
        'message': 'Entity created successfully',
    },
    constants.HTTP_409_CONFLICT: {
        'response_code': constants.HTTP_409_CONFLICT,
        'http_code': constants.HTTP_409_CONFLICT,
        'response_type': ResponseTypeEnum.error,
        'message': 'Entity already exists',
    }

})
