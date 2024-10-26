import logging
import inject

from service_common.utils import (
    verify_password,
    create_access_token
)
from service_common.error import ApplicationError
from service_common.utils import respond
from service_common.settings import CoreSettings
from service_common.service.base import BaseService

from auth_service import constants
from auth_service.service.unit_of_work import UnitOfWork
from auth_service.api.schema.login import AuthRequest, AuthResponse

logger = logging.getLogger(__name__)


class AuthenticatorService(BaseService):

    @inject.autoparams('uow')
    def __init__(self, uow: UnitOfWork, current_user_id: str = None):
        super(AuthenticatorService, self).__init__(current_user_id=current_user_id)
        self.uow = uow
        self.uow.current_user_id = current_user_id

    def verify_password(self, user_name: str, password: str):
        with self.uow:
            user = self.uow.users.find_by_email(user_name)
            if not user:
                raise ApplicationError(response_code=constants.USER_NOT_REGISTERED, message="User does not exists")

            if user and verify_password(password, user.password_hash):
                access = {}
                data = {'sub': user.public_id}
                access['token'] = create_access_token(data)
                access['t_type'] = 'access'
                access['user_id'] = user.id
                access['user_public_id'] = user.public_id
                access['is_revoked'] = False
                access['user_type_map'] = self.uow.users.get_user_map(user)

                self.uow.tokens.add_token(user.public_id, access)
                return AuthResponse(
                    email=user.email, phone=user.mobile, access_token=access.get('token'),
                    public_id=user.public_id, user_type=user.user_type,
                    first_name=user.first_name, middle_name=user.middle_name,
                    last_name=user.last_name, user_type_map=access['user_type_map'] or []
                )

            raise ApplicationError(response_code=constants.HTTP_401_UNAUTHORIZED, message="User password is wrong")

    def logout(self) -> None:
        """

        :return:
        """
        with self.uow:
            self.uow.tokens.delete(self.current_user_id)

    def send_otp(self, phone_number: str):
        with self.uow:
            user = self.uow.users.find_by_mobile(phone_number)
            if not user:
                raise ApplicationError(response_code=constants.USER_NOT_REGISTERED, message="User does not exists")
            # @todo: Implement OTP service call

    def verify_otp(self, phone_number: str, otp: str):
        with self.uow:

            user = self.uow.users.find_by_mobile(phone_number)
            if not user:
                raise ApplicationError(response_code=constants.USER_NOT_REGISTERED, message="User does not exists")

            fa_phone = user.mobile
            if user.user_type == 'FARMER':
                # Farmer will login with It's FA's last 4 digits of mobile number
                fa = self.uow.users.find_by_public_id(user.created_by)
                fa_phone = fa.mobile or ''
            settings = inject.get_injector().get_instance(CoreSettings)
            if otp != fa_phone[-4:]:
                if not (settings.current_env in ['DEV', 'LOCAL'] and otp == '0000'):
                    raise ApplicationError(response_code=constants.HTTP_401_UNAUTHORIZED, message="Invalid OTP")

            access = {}
            data = {'sub': user.public_id}
            access['token'] = create_access_token(data)
            access['t_type'] = 'access'
            access['user_type'] = user.user_type
            access['user_id'] = user.id
            access['user_public_id'] = user.public_id
            access['is_revoked'] = False
            access['user_type_map'] = self.uow.users.get_user_map(user)

            self.uow.tokens.add_token(user.public_id, access)
            return AuthResponse(
                email=user.email, phone=user.mobile, access_token=access.get('token'),
                public_id=user.public_id, user_type=user.user_type,
                first_name=user.first_name, middle_name=user.middle_name,
                last_name=user.last_name, user_type_map=access['user_type_map'] or []
            )
