import typing
import inject
from enum import Enum

from pydantic import BaseModel, Field
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import get_authorization_scheme_param

from service_common.settings import CoreSettings
from service_common.enums import OrderEnum


class ResponseType(str, Enum):
    success: str = 'SUCCESS'
    error: str = 'ERROR'
    warning: str = 'WARNING'
    info: str = 'INFO'


class ApiInfoSchema(BaseModel):
    name: str = Field(..., title="Name", description="Name of the app")
    version: str = Field(..., title="Version", description="Version of the app")
    api_version: str = Field(..., title="API Version", description="Version of the API")
    message: str = Field(..., title="Message", description="Welcome message")


class ResponseSchema(BaseModel):
    response_code: int = Field(...,
                               title="Response Code",
                               description="Unique response "
                                           "code specific to error")
    response_type: ResponseType = Field(None,
                                        title="Response Type",
                                        description="Response type")
    message: str = Field(..., title="Message",
                         description="Message may be useful for user")
    description: typing.Optional[str] = Field(default=None,
                                              title="Description",
                                              description="Debug "
                                                          "information for developer")
    public_id: typing.Optional[str] = Field(default=None,
                                            title="Entity Public ID",
                                            description="Public ID of the entity "
                                                        "on which currently we are operating on")

    def __init__(self, **kwargs):
        super(ResponseSchema, self).__init__(**kwargs)
        settings = inject.instance(CoreSettings)
        if settings.current_env == 'PROD':
            self.description = None


class ImageResponseSchema(ResponseSchema):
    image_url: str = None


class BaseRequestSchema(BaseModel):
    # device_id: typing.Optional[str] = None
    pass


class BaseRelatedRecordsSchema(BaseModel):
    public_id: str = Field(default=None, title="Public ID of related record")


class AuthenticationSchema(OAuth2PasswordBearer):

    def __init__(self, **kwargs):
        config = inject.instance(CoreSettings)
        super(AuthenticationSchema, self).__init__(
            tokenUrl=config.token_url,
            **kwargs
        )

    async def __call__(self, request: Request) -> typing.Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)
        return token


class PaginationResponseSchema(BaseModel):
    data: typing.List[dict] = Field(default_factory=list, title="List of records")
    total_count: int = Field(default=0, title="Total record count")
    page_size: int = Field(default=10, title="Records per page")
    page: int = Field(default=1, title="Current Page Number")
    total_pages: int = Field(default=1, title="Total number of pages")
    has_next_page: bool = Field(default=False, title="Has next page")
    has_prev_page: bool = Field(default=False, title="Has previous page")


class SearchPaginatedRequestSchema(BaseModel):
    search: str = Field(default=None, title="Filter records")
    page: int = Field(default=1, title="Requested page number", gt=0)
    page_size: int = Field(default=10, title="Number of records per page", gt=0)
    order_by: str = Field(default='created_at', title="Sort records by")
    order: OrderEnum = Field(default=OrderEnum.desc, title="Sort order")


class PaginatedRequestSchema(BaseModel):
    page: int = Field(default=1, title="Requested page number", gt=0)
    page_size: int = Field(default=10, title="Number of records per page", gt=0)
    order_by: str = Field(default='created_at', title="Sort records by")
    order: OrderEnum = Field(default=OrderEnum.desc, title="Sort order")


class OnlyPaginatedRequestSchema(BaseModel):
    page: int = Field(default=1, title="Requested page number", gt=0)
    page_size: int = Field(default=10, title="Number of records per page", gt=0)


class DropdownValue(BaseModel):
    value: str = Field(title="Value of the record")
    title: typing.Any = Field(title="Name to display")


class DropdownResponseSchema(BaseModel):
    __root__: typing.List[DropdownValue] = Field(default_factory=list)


class DropdownPaginationResponseSchema(PaginationResponseSchema):
    data: typing.List[DropdownValue] = Field(default_factory=list)


class ImageExtensionEnum(str, Enum):
    jpg = "jpg"
    png = "png"
    jpeg = "jpeg"


class ImageFile(BaseModel):
    base64_str: str
    extension: ImageExtensionEnum
    name: typing.Optional[str]

