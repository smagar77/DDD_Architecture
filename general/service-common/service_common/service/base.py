from service_common.unit_of_work import AbstractUnitOfWork
from service_common.context_vars import set_current_user_uuid, reset_current_user_uuid


class BaseService:
    current_user_id: str = None

    def __init__(self, current_user_id: str = None):
        self.current_user_id = current_user_id
        self._ctx_token = set_current_user_uuid(current_user_id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        reset_current_user_uuid(self._ctx_token)
