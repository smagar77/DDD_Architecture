from fastapi import Depends, Form
from service_common.router import APIRouter
from service_common.schema import ResponseSchema, AuthenticationSchema

from auth_service.api.schema import login
from auth_service import constants
from service_common.utils import respond
from service_common.deps import get_authorised_user

from auth_service.service.authenticator import AuthenticatorService

router = APIRouter(tags=['Authentication'])


@router.post('/auth', response_model=login.AuthResponse)
async def login_request(
        user_login: login.AuthRequest
):
    service = AuthenticatorService()
    return service.verify_password(user_login.user_name, password=user_login.password)


@router.delete('/auth', response_model=ResponseSchema)
async def logout_request(
        current_user_id: str = Depends(get_authorised_user)
):
    service = AuthenticatorService(current_user_id=current_user_id)
    service.logout()
    return respond(constants.RESPONSE_OK, message="Logged out successfully")


@router.post('/otp', response_model=ResponseSchema)
async def send_otp(
        user_login: login.OtpRequestSchema
):
    service = AuthenticatorService()
    service.send_otp(user_login.phone)
    return respond(constants.RESPONSE_OK, message="OTP Has been sent successfully")


@router.put('/otp', response_model=login.AuthResponse)
async def verify_otp(
        user_login: login.VerifyOTPSchema
):
    service = AuthenticatorService()
    return service.verify_otp(user_login.phone, user_login.otp)


@router.post('/token', response_model=login.AuthResponse, include_in_schema=False)
async def get_token(
        username: str = Form(), password: str = Form()
):
    """
    This API is used by OpenAPI specification only, not meant to be used by the other users
    :param username:
    :param password:
    :return:
    """
    service = AuthenticatorService()
    if username.find('@') > 0:
        # If email is provided, we will look for the Password authentication
        return service.verify_password(username, password)
    else:
        # Consider we want to do the Phone OTP based authentication
        # Before getting Authenticated Please call POST auth/otp API manually
        return service.verify_otp(username, password)
