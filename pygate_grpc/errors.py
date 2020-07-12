import grpc
import logging

from pygate_grpc.exceptions import GRPCNotAvailableException

logger = logging.getLogger(__name__)


def error_handler(func):
    """A decorator to handle errors"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except grpc._channel._InactiveRpcError as e:
            err_to_raise = e
            if err_to_raise.code() == grpc.StatusCode.UNAVAILABLE:
                err_to_raise = GRPCNotAvailableException(e)
        raise err_to_raise

    return wrapper


class ErrorHandlerMeta(type):
    """
    A metaclass to embed a global error handler for class methods.

    Mainly used to abstract tout GRPC exceptions.
    """

    def __new__(cls, classname, bases, classdict):

        for attr, item in classdict.items():
            if callable(item):
                classdict[attr] = error_handler(item)  # replace method by wrapper

        return type.__new__(cls, classname, bases, classdict)
