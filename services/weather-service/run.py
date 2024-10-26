import sys

import inject
import uvicorn                      # type: ignore

from os.path import abspath, join

# Adjust the paths
sys.path.insert(0, abspath(join(__file__)))
print(abspath(join(__file__)))
# Run the ASGI server
from weather_service.app.bootstrap import api
from service_common.settings import CoreSettings
settings = inject.instance(CoreSettings)


uvicorn.run(
    api, host=settings.app_host, port=settings.app_port, reload=bool(settings.current_env.lower()=='local')
)
