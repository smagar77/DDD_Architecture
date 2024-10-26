import typing
import inject
import base64

from service_common.service.storage import Storage


class BaseImageStore:
    backend: Storage = None
    path_prefix = None

    @inject.autoparams('backend')
    def __init__(self, backend: Storage):
        self.backend = backend

    def get_file_path(self, file_name: str):
        """
        Returns full path relative to bucket

        :param file_name:
        :return:
        """
        return f"{self.path_prefix}/{file_name}"

    def get_url(self, file_name: str):
        """
        Returns Access URl for the given image/document
        :param file_name:
        :return:
        """
        file_path = self.get_file_path(file_name)
        return self.backend.get_url(file_path)

    def put(self, file_name: str, file_content: typing.Union[str, bytearray, bytes],
            base64_encoded: bool = True):
        """
        Upload the file to file Store

        :param file_name:
        :param file_content:
        :param base64_encoded:
        :return:
        """
        file_path = self.get_file_path(file_name)
        if base64_encoded:
            # Decode base64 encoded string
            file_content = base64.b64decode(file_content)
        self.backend.put(file_path, file_content=file_content)

    def delete(self, file_name: str):
        file_path = self.get_file_path(file_name)
        self.backend.delete(file_path)


class ProfileImageStore(BaseImageStore):
    path_prefix = 'profile-photos'

