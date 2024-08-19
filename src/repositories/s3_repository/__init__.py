import logging
from typing import TypeVar

from usecases.errors import S3Error

T = TypeVar("T")


def handle_s3_errors(method):  # noqa
    def inner(self, *args, **kwargs):  # noqa
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            logging.error(f"S3 Error: {e}")
            raise S3Error(e) from e

    return inner
