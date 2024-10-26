import typing
import base64

from abc import abstractmethod
from logging import getLogger


logger = getLogger(__name__)


class Storage:
    @abstractmethod
    def get_url(self, file_path, expires: int = None):
        ...

    @abstractmethod
    def get(self, file_path: str, ):
        ...

    @abstractmethod
    def put(self, file_path: str, file_content: typing.Union[str, bytearray, bytes]):
        ...

    def put_base64_file(self, file_path: str, file_content: str):
        """
        Saves base64 encoded file to document store
        :param file_path:
        :param file_content:
        :return:
        """
        # Decode base64 encoded string
        file_content = base64.b64decode(file_content)
        self.put(file_path, file_content=file_content)

    def delete(self, file_path: str):
        ...
