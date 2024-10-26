import typing
import inject
from service_common.settings import CoreSettings

from auth_service.settings import Settings

from . import dependency


def init_app():
    from service_common.bootstrap import create_app
    # Loading apps
    from auth_service.api.login import router as auth_ends
    from auth_service.api.user import router as user_ends

    api_ = create_app(typing.cast(Settings, inject.instance(CoreSettings)))
    return api_


# Create the FAST API app
api = init_app()
