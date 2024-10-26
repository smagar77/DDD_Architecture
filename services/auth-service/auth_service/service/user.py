import inject

from service_common.service.base import BaseService
from service_common.domains import User
from service_common.domains import SearchPaginatedParameters
from service_common.error import ApplicationError

from auth_service.service.unit_of_work import UnitOfWork
from auth_service import constants


class UserService(BaseService):

    @inject.autoparams('uow')
    def __init__(self, uow: UnitOfWork, current_user_id: str = None):
        super(UserService, self).__init__(current_user_id=current_user_id)
        self.uow = uow
        self.uow.current_user_id = current_user_id

    async def list_users(self, paginate: SearchPaginatedParameters) -> dict:
        result = []
        with self.uow:

            paginated = self.uow.users.get_paginated_result(
                **paginate.dict(),
            )
            for item in paginated.get('data', []) or []:
                result.append(User.from_orm(item).dict())
            paginated['data'] = result
        return paginated

    async def create_user(self, user: User):
        with self.uow:
            self.uow.users.add(user.dict(exclude_none=True))
            self.uow.commit()

    async def update_user(self, user: User):
        with self.uow:
            record = self.uow.users.find_by_public_id(user.public_id)
            if self.uow.users.check_user_exists(mobile=user.mobile, email=user.email,
                                                public_id=user.public_id):
                raise ApplicationError(response_code=constants.HTTP_409_CONFLICT,
                                       message="User already exists with Mobile number or Email")
            user_rec = User.from_orm(record)
            user_rec = user_rec + user
            data = user_rec.dict(exclude={'public_id'}, exclude_unset=True)
            self.uow.users.update_by(values=data, where={'public_id': user.public_id})
            self.uow.commit()

    async def get_dashboard(self):
        with self.uow:
            dashboard = {
                'FARMER': {
                    'name': 'FARMER',
                    'count': 0
                },
                'FPO': {
                    'name': 'FPO',
                    'count': 0
                },
                'BUYER': {
                    'name': 'BUYER',
                    'count': 0
                },
                'FIELD_AGENT': {
                    'name': 'FIELD_AGENT',
                    'count': 0
                },
                'ADMIN': {
                    'name': 'ADMIN',
                    'count': 0
                },
                'SELLER': {
                    'name': 'SELLER',
                    'count': 0
                },
            }
            if not self.uow.current_user:
                raise ApplicationError(response_code=constants.RECORD_NOT_FOUND, message='User not found')
            owner_filter = {}
            if self.uow.current_user.user_type not in ['ADMIN', 'SUPER_ADMIN']:
                owner_filter = {
                    'created_by': self.current_user_id
                }
            for entity in self.uow.users.get_users_count_by_type(**owner_filter):
                name = entity[0]
                dashboard[name] = {'name': entity[0], 'count': entity[1]}

            return list(dashboard.values())
