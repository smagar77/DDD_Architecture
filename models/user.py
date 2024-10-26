"""Class definition for User model."""

from service_common.model import UserBaseModel, Base


class UserModel(Base, UserBaseModel):
    """User model for storing logon credentials and other details."""

    __tablename__ = "site_user"
