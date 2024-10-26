import typing

import inject
import logging
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from pymongo import MongoClient

from service_common.settings import CoreSettings
from service_common.adapter.redis_adapter import BaseBackend
from service_common.adapter.redis_adapter import RedisBackend
from service_common.service.storage_s3 import StorageS3, Storage

from weather_service.settings import Settings
from weather_service.error_conf import ErrorConfig
from weather_service.service.unit_of_work import UnitOfWork
from weather_service.service.acuweather import AcuWeatherService


logger = logging.getLogger(__name__)


@lru_cache
def get_settings():
    return Settings()


def sql_alchemy_session_factory() -> sessionmaker:
    """"
    SQLAlchemy Session Maker
    """
    settings = get_settings()
    engine = create_engine(
        settings.sqlalchemy_uri
    )
    logger.info("Initializing SQLAlchemy Session Maker")
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_backend() -> BaseBackend:
    """
    Gets the object store Backend
    :return:
    """
    logger.info("Initializing Redis Backend")
    settings = get_settings()
    try:
        backend = RedisBackend(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_pass,
            username=settings.redis_user
        )
    except Exception as ex:
        logger.fatal(f"Unable to instantiate RedisBackend with Exception {ex}",
                     exc_info=True)
        backend = BaseBackend()

    return backend


def get_s3_storage() -> StorageS3:
    logger.info("Initializing s3-bucket storage")
    settings = get_settings()
    return StorageS3(settings)


def get_weather_service() -> AcuWeatherService:
    settings = get_settings()
    return AcuWeatherService(api_key=settings.weather_api_key)


def get_mongo_client() -> typing.Optional[MongoClient]:
    settings = get_settings()
    if not settings.mongo_db_uri:
        return None
    try:
        return MongoClient(
            settings.mongo_db_uri
        )
    except Exception:
        return None


def configure_dependency(binder: inject.Binder):
    # bind instances
    binder.bind(CoreSettings, get_settings())
    binder.bind(BaseBackend, get_backend())
    binder.bind(AcuWeatherService, get_weather_service())

    # Singleton Error configuration
    binder.bind_to_constructor(ErrorConfig, ErrorConfig)
    binder.bind_to_constructor(Storage, get_s3_storage)

    # Always return the new SQLAlchemy Session
    binder.bind_to_provider(Session, sql_alchemy_session_factory())
    binder.bind_to_provider(MongoClient, get_mongo_client)
    binder.bind_to_provider(UnitOfWork, UnitOfWork)


inject.configure(configure_dependency)
