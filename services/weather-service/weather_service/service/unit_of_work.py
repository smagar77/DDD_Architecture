from service_common.unit_of_work import SqlAlchemyUnitOfWork
from service_common.repository import UserBaseSqlAlchemyRepository
from weather_service.repository.weather_cache import WeatherCacheRepository
from service_common.domains import User


class UnitOfWork(SqlAlchemyUnitOfWork):
    """

    """
    users: UserBaseSqlAlchemyRepository = None
    cache: WeatherCacheRepository = None

    def __init__(self, *args, **kwargs):
        """

        """
        super(UnitOfWork, self).__init__(*args, **kwargs)

    def __enter__(self):
        super(UnitOfWork, self).__enter__()
        # initialize repositories after connecting to DB
        self.users = UserBaseSqlAlchemyRepository(self.session)
        self.cache = WeatherCacheRepository()

        if (
                self.current_user_id
                and (not self.current_user
                     or self.current_user.public_id != self.current_user_id)
        ):
            # Load current user
            user = self.users.find_by_public_id(self.current_user_id)
            self.current_user: User = User.from_orm(user)
