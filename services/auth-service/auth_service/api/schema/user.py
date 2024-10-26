import datetime
import typing

from pydantic import BaseModel, Field

from service_common.schema import BaseRequestSchema, PaginationResponseSchema, SearchPaginatedRequestSchema
from service_common.enums import UserTypeEnum


class UserRequestSchema(BaseRequestSchema):
    email: str = None
    mobile: str = None
    password: typing.Optional[str] = None
    user_type: typing.Optional[UserTypeEnum] = Field(default=UserTypeEnum.field_agent)
    first_name: str
    middle_name: typing.Optional[str] = None
    last_name: str


class UserResponseSchema(BaseModel):
    email: str = None
    mobile: str = None
    public_id: str = None
    user_type: UserTypeEnum = Field(default=UserTypeEnum.field_agent)
    first_name: str = None
    middle_name: typing.Optional[str] = None
    last_name: str = None


class UserListResponseSchema(BaseModel):
    __root__: typing.List[UserResponseSchema] = Field(default_factory=list)


class UserPaginationResponseSchema(PaginationResponseSchema):
    data: typing.List[UserResponseSchema] = Field(default_factory=list, title="Farm records")


class UserSearchPaginatedRequestSchema(SearchPaginatedRequestSchema):
    user_type: UserTypeEnum = UserTypeEnum.field_agent


class EntitySchema(BaseModel):
    name: str = Field(default=None, title="Name of the entity")
    count: int = Field(default=0, title="Count of the entity", ge=0)


class UserDashboardSchema(BaseModel):
    entities: typing.List[EntitySchema] = Field(title="List of entities in dashboard")
    first_name: str = Field(default=None, title="First name of the user")
    middle_name: str = Field(default=None, title="Middle name of the user")
    last_name: str = Field(default=None, title="Last name of the user")
    user_type: UserTypeEnum = Field(default=None, title="User Type")
