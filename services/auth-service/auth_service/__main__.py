import sys

import inject
import uvicorn  # type: ignore

from os.path import abspath, join

# Adjust the paths
sys.path.insert(0, abspath(join(__file__, "../", "../")))

# Run the ASGI server
from auth_service.app.bootstrap import api
from service_common.settings import CoreSettings

settings = inject.instance(CoreSettings)

if __name__ == '__main__':
    uvicorn.run(
        api, host=settings.app_host, port=settings.app_port
    )
