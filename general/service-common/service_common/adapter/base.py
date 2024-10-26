"""The Core module
Implements the common base classes utilities
"""
import sys
from itertools import islice
from itertools import zip_longest
import os


class Singleton(type):
    """Singleton Metaclass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseBackend(metaclass=Singleton):
    """Provides Basic features for the backend

    """

    def __init__(self, *args, **kwargs):
        super(BaseBackend, self).__init__()

    def set_dict(self, key, data, **kwargs):
        raise NotImplementedError

    def get_dict(self, key):
        raise NotImplementedError

    def set_list(self, key: str, data: list, **kwargs):
        raise NotImplementedError

    def get_list(self, key: str):
        raise NotImplementedError

    def set_str(self, key: str, data: str, **kwargs):
        raise NotImplementedError

    def get_str(self, key: str):
        raise NotImplementedError

    def find_keys(self, pattern):
        raise NotImplementedError

    def scan(self, match_: str, **kwargs) -> str:
        raise NotImplementedError

    def delete(self, *keys):
        raise NotImplementedError
