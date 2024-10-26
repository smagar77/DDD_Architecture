from fastapi import status
from service_common.error_conf import ErrorConfig
from service_common.enums import ResponseTypeEnum

from . import constants


# Authorization App related messages
ErrorConfig.extend({
    constants.USER_TOKEN_EXPIRED: {
        'response_code': constants.USER_TOKEN_EXPIRED,
        'http_code': status.HTTP_401_UNAUTHORIZED,
        'response_type': ResponseTypeEnum.error,
        'message': 'User token expired',
    },
    constants.USER_TOKEN_ERROR: {
        'response_code': constants.USER_TOKEN_ERROR,
        'http_code': status.HTTP_401_UNAUTHORIZED,
        'response_type': ResponseTypeEnum.error,
        'message': 'User token is not valid',
    },
    constants.USER_TOKEN_INVALID: {
        'response_code': constants.USER_TOKEN_INVALID,
        'http_code': status.HTTP_401_UNAUTHORIZED,
        'response_type': ResponseTypeEnum.error,
        'message': 'User token is not valid',
    },
    constants.AUTHORIZATION_REQUIRED: {
        'response_code': constants.AUTHORIZATION_REQUIRED,
        'http_code': status.HTTP_401_UNAUTHORIZED,
        'response_type': ResponseTypeEnum.error,
        'message': 'Authorization is required for this action',
    },
    constants.OTP_VERIFICATION_LIMIT_REACHED: {
        'response_code': constants.OTP_VERIFICATION_LIMIT_REACHED,
        'http_code': status.HTTP_429_TOO_MANY_REQUESTS,
        'response_type': ResponseTypeEnum.error,
        'message': 'OTP Verification request limit reached. Please try after 5 minutes.',
    },
    constants.OTP_INVALID: {
        'response_code': constants.OTP_INVALID,
        'http_code': status.HTTP_417_EXPECTATION_FAILED,
        'response_type': ResponseTypeEnum.error,
        'message': 'Wrong OTP Entered',
    },
    constants.USER_NOT_REGISTERED: {
        'response_code': constants.USER_NOT_REGISTERED,
        'http_code': status.HTTP_404_NOT_FOUND,
        'response_type': ResponseTypeEnum.error,
        'message': 'User is not registered',
    },
    constants.RECORD_NOT_FOUND: {
        'response_code': constants.RECORD_NOT_FOUND,
        'http_code': status.HTTP_404_NOT_FOUND,
        'response_type': ResponseTypeEnum.error,
        'message': 'Record not found',
    },
    constants.MISSING_DATA: {
        'response_code': constants.MISSING_DATA,
        'http_code': status.HTTP_417_EXPECTATION_FAILED,
        'response_type': ResponseTypeEnum.error,
        'message': 'Data is missing in request',
    },
    constants.RESPONSE_OK: {
        'response_code': constants.RESPONSE_OK,
        'http_code': status.HTTP_200_OK,
        'response_type': ResponseTypeEnum.success,
        'message': 'Operation performed with success',
    },
    constants.HTTP_409_CONFLICT: {
        'response_code': constants.HTTP_409_CONFLICT,
        'http_code': status.HTTP_409_CONFLICT,
        'response_type': ResponseTypeEnum.error,
        'message': 'Record already exists',
    },
})
