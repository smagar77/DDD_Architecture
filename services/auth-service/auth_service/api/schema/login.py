import typing
from pydantic import BaseModel, Field

from service_common.schema import BaseRequestSchema
from service_common.enums import UserTypeEnum


class AuthRequest(BaseRequestSchema):
    user_name: str
    password: str


class OtpRequestSchema(BaseRequestSchema):
    phone: str


class UserTypeMap(BaseModel):
    user_type: UserTypeEnum = None
    public_id: str = None


class AuthResponse(BaseRequestSchema):
    email: typing.Optional[str] = None
    phone: str
    public_id: str
    access_token: str
    user_type: UserTypeEnum
    first_name: str = None
    middle_name: typing.Optional[str] = None
    last_name: str = None

    user_type_map: typing.List[UserTypeMap] = Field(default_factory=list)


class VerifyOTPSchema(BaseRequestSchema):
    phone: str
    otp: str

