import json
import typing
from pydantic import BaseSettings, PostgresDsn, validator

SQLITE_DEV = "sqlite:///data_dev.db"
SQLITE_TEST = "sqlite:///data_test.db"
SQLITE_STAGE = "sqlite:///data_stage.db"


class CoreSettings(BaseSettings):
    """

    """
    app_title: str
    app_version: str
    api_version: str
    app_description: str

    app_port: int = 8080
    app_host: str = '127.0.0.1'
    app_base_url: str = None
    base_url: str = None
    root_path: str = ""
    openapi_url: str = '/openapi.json'
    log_file: str = 'agreco.log'
    current_env: str = 'LOCAL'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30
    token_url: str = 'token'
    shared_secret_key: str = None
    app_secret_key: str = None

    force_https: bool = False
    cors_origins: typing.Set[str] = {"http://127.0.0.1:8888", "http://127.0.0.1:3000", "https://dev.agreco.in"}

    db_server: str = None
    db_user: str = None
    db_pass: str = None
    db_name: str = None
    sqlalchemy_uri: str = None

    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_user: str = None
    redis_pass: str = None

    aws_access_key_id: str = None
    aws_secret_access_key: str = None
    s3_bucket_region: str = 'ap-south-1'
    pre_signed_expiry: int = 36000
    s3_bucket_name: str = 'demo'

    mongo_server: str = None
    mongo_port: int = 27017
    mongo_user: str = None
    mongo_pass: str = None
    mongo_db_name: str = None
    mongo_ssl: bool = False
    mongo_ca_file: str = None
    mongo_params: str = None
    mongo_db_uri: str = None

    weather_api_key: str = None

    class Config:
        # Load from .env file
        env_file: str = '.env'

    @property
    def redis_dsn(self):
        user_pass = [self.redis_user, self.redis_pass]
        user_pass = ":".join(user_pass)
        if user_pass:
            return f"redis://{user_pass}@{self.redis_host}:{self.redis_port}"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}"

    @validator("sqlalchemy_uri", pre=True)
    def assemble_db_connection(cls, v: typing.Optional[str], values: typing.Dict[str, typing.Any]) -> typing.Any:
        if isinstance(v, str):
            return v
        if values.get("db_server"):
            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("db_user"),
                password=values.get("db_pass"),
                host=values.get("db_server"),
                path=f"/{values.get('db_name') or ''}",
            )

        return SQLITE_DEV

    @validator("mongo_db_uri", pre=True)
    def assemble_mongo_connection(cls, v: typing.Optional[str], values: typing.Dict[str, typing.Any]) -> typing.Any:
        if isinstance(v, str):
            return v
        serv = values.get("mongo_server")
        if serv:
            user = values.get("mongo_user")
            pass_ = values.get("mongo_pass")
            port = values.get("mongo_port")
            params = []
            enable_ssl = values.get("mongo_ssl", False)
            if enable_ssl:
                params.append("ssl=true")
                cert = values.get('mongo_ca_file')
                params.append(f'tlsCAFile={cert}')
            else:
                params.append("ssl=false")
            extra = values.get("mongo_params")
            if extra:
                params.append(extra)
            params = '&'.join(params)
            value = f"mongodb://{user}:{pass_}@{serv}:{port}/?{params}"
            return value
