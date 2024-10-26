import typing
import os

from logging import getLogger

import inject

from app.core.config import Settings
from app.core.singleton_meta import SingletonMeta
from app.core.services.storage import Storage

logger = getLogger(__name__)


class LocalFileStorage(Storage, metaclass=SingletonMeta):
    bade_path: str = None

    @inject.autoparams('settings')
    def __init__(self, settings: Settings):
        self.bade_path = settings.local_storage_base_path

    def get_url(self, file_path, expires: int = None):
        pass

    def get(self, file_path: str):
        with open(os.path.join(self.bade_path, file_path), 'r') as file_stream:
            return file_stream.read(), None

    def put(self, file_path: str, file_content: typing.Union[str, bytearray, bytes]):
        with open(os.path.join(self.bade_path, file_path), 'w') as file_stream:
            return file_stream.write(file_path)
