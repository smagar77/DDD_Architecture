from fastapi import Depends, Form
from service_common.router import APIRouter
from service_common.schema import ResponseSchema, SearchPaginatedRequestSchema
from service_common.domains import UserSearchPaginatedParameters

from auth_service.api.schema import user
from auth_service import constants
from service_common.utils import respond
from service_common.deps import get_authorised_user

from auth_service.service.user import UserService
from auth_service import domain

router = APIRouter(prefix='/user', tags=['User Management'])


@router.get("", response_model=user.UserPaginationResponseSchema)
async def get_users(
        paginate: user.UserSearchPaginatedRequestSchema = Depends(user.UserSearchPaginatedRequestSchema),
        current_user: str = Depends(get_authorised_user)
):
    service = UserService(current_user_id=current_user)
    paginate = UserSearchPaginatedParameters(**paginate.dict())
    result = await service.list_users(paginate)
    return result


@router.post("", response_model=ResponseSchema)
async def create_user(user_form: user.UserRequestSchema, current_user: str = Depends(get_authorised_user)):
    service = UserService(current_user_id=current_user)
    entity = domain.UserDb(**user_form.dict(exclude_none=True, exclude={'device_id'}))
    entity.set_pass_hash(user_form.password)
    await service.create_user(entity)
    return respond(constants.HTTP_201_CREATED)


@router.patch("/{public_id}", response_model=ResponseSchema)
async def update_user(
        public_id: str, user_form: user.UserRequestSchema, current_user: str = Depends(get_authorised_user)
):
    service = UserService(current_user_id=current_user)
    entity = domain.User(**user_form.dict(exclude_none=True, exclude={'device_id'}))
    entity.public_id = public_id
    await service.update_user(entity)
    return respond(constants.HTTP_200_OK)


@router.get("/dashboard", response_model=user.UserDashboardSchema)
async def get_user_dashboard(current_user: str = Depends(get_authorised_user)):
    service = UserService(current_user_id=current_user)
    entities = await service.get_dashboard()
    return user.UserDashboardSchema(
        entities=entities,
        **service.uow.current_user.dict(include={'first_name', 'middle_name', 'last_name', 'user_type'})
    )
