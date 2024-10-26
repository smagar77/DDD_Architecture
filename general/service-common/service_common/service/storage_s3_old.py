import base64
import typing
import inject
import boto3

from abc import ABC, abstractmethod
from logging import getLogger
from service_common.settings import CoreSettings
from botocore.exceptions import ClientError
from botocore.config import Config
from service_common.singlton_meta import SingletonMeta


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

    @abstractmethod
    def delete(self, file_path: str):
        ...


class StorageS3(Storage, metaclass=SingletonMeta):

    service_name: str = 's3'
    signature_version: str = 's3v4'
    bucket_name: str = None

    def __init__(self,
                 settings: CoreSettings, expiry: int = None,
                 signature_version: str = 's3v4'):

        self._expiry = expiry or settings.pre_signed_expiry
        self.signature_version = signature_version
        self.bucket_name = settings.s3_bucket_name

        # Initialize the s3 boto client
        s3_conf = Config(
            region_name=settings.s3_bucket_region,
            signature_version=self.signature_version
        )
        self._client = boto3.client(
            self.service_name,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            config=s3_conf
        )

    def get_url(self, file_path, expires: int = None):
        """

        :param file_path:
        :param expires:
        :return:
        """

        if not expires:
            expires = self._expiry

        params = {
            'Bucket': self.bucket_name,
            'Key': file_path,
        }

        try:
            return self._client.generate_presigned_url(
                    ClientMethod='get_object',
                    Params=params,
                    ExpiresIn=expires
                )
        except ClientError as e:
            logger.error(f"Exception: {e}", exc_info=True)
            raise e

    def put(self, file_path: str, file_content: typing.Union[str, bytearray, bytes]):
        """

        :param file_path:
        :param file_content:
        :return:
        """
        self._client.put_object(
            Bucket=self.bucket_name,
            Key=file_path,
            Body=file_content
        )

    def get(self, file_path: str):
        """

        :param file_path:
        :return:
        """
        try:
            response = self._client.get_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return response['Body'].read()
        except ClientError as e:
            logger.error(e)
            raise e

    def delete(self, file_path: str):
        """

        :param file_path:
        :return:
        """
        try:
            self._client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
        except ClientError as e:
            logger.error(e)
            raise e
