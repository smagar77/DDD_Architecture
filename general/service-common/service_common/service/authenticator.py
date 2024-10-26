from service_common.unit_of_work import AbstractUnitOfWork


class Authentication:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def verify_token(self, token: str):
        pass
