import re
import datetime

from uuid import uuid4
from sqlalchemy import String, Integer, DateTime, Column, TIMESTAMP, Boolean
from sqlalchemy import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from service_common.utils import get_password_hash, verify_password
from service_common.datetime_util import utc_now, make_tzaware, get_local_utcoffset, localized_dt_string


class CoreModel:

    id: int = Column(Integer, primary_key=True)
    created_at: datetime.datetime = Column(DateTime, server_default=func.now())
    modified_at: datetime.datetime = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    public_id = Column(String(36), unique=True, default=lambda: str(uuid4()))
    is_deleted = Column(Boolean(), default=False)
    created_by: str = Column(String(36))
    modified_by: str = Column(String(36))


class UserBaseModel(CoreModel):
    email = Column(String(255), unique=True, nullable=True)
    mobile = Column(String(10), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    registered_on = Column(DateTime, default=utc_now)
    user_type = Column(String, nullable=False, default='SUPER_ADMIN')
    public_id = Column(String(36), unique=True, default=lambda: str(uuid4()))
    first_name = Column(String(255), nullable=True)
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)

    def __repr__(self):
        return (
            f"<User email={self.email}, mobile={self.mobile}, public_id={self.public_id}, user_type={self.user_type}>"
        )

    @hybrid_property
    def registered_on_str(self):
        registered_on_utc = make_tzaware(
            self.registered_on, use_tz=datetime.timezone.utc, localize=False
        )
        return localized_dt_string(registered_on_utc, use_tz=get_local_utcoffset())

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = get_password_hash(password)

    def check_password(self, password):
        return verify_password(password, self.password_hash)

    @property
    def name(self):
        data = []
        for key in []:
            value = getattr(self, key, None)
            if value:
                data.append(value)
        return ' '.join(data) if data else None


class CoreRelationModel:
    id: int = Column(Integer, primary_key=True)
    created_at: datetime.datetime = Column(DateTime, server_default=func.now())
    modified_at: datetime.datetime = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    is_deleted = Column(Boolean(), default=False)
    created_by: str = Column(String(36))
    modified_by: str = Column(String(36))


@as_declarative()
class Base:
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
