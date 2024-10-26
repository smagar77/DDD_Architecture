import abc
import logging
import inject
from sqlalchemy.orm.session import Session
from service_common.adapter.base import BaseBackend
from service_common.adapter.redis_token import TokenRedisRepository

logger = logging.getLogger(__name__)


def default_session_factory() -> Session:
    """
    Default DB Session Factory
    :return:
    """
    logger.info("Creating databse Session")
    return inject.instance(Session)


class AbstractUnitOfWork(abc.ABC):
    # Database session
    session: Session = None
    tokens: TokenRedisRepository = None

    def __init__(self):
        self.tokens = TokenRedisRepository()

    def __enter__(self) -> 'AbstractUnitOfWork':
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """
    SQLAlchemy Unit of Work
    """

    current_user_id: str = None
    current_user = None

    def __init__(self, session: Session = None, session_factory=default_session_factory):
        """
        Either the session object or session_factory need to be provided
        If session object is passed it will be passed down to the repository
        If Session object is not provided then it will try to create with the session factory
        And then passed it down to the repository
        :param session: sqlalchemy.orm.Session:
        :param session_factory: Callable: which returns the session object
        """
        self.session = session
        self.session_factory = session_factory
        self.close_on_exit = False
        super(SqlAlchemyUnitOfWork, self).__init__()

    def __enter__(self):
        """
        Starts the context manager for the
        :return:
        """
        super().__enter__()
        if not self.session:
            # Session is not initialized so creating new session
            self.session = self.session_factory()  # type: Session
            self.close_on_exit = True
        return self

    def __exit__(self, *args):
        super().__exit__(*args)
        if self.close_on_exit:
            # Close the session only if it is started in the context manager
            self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
