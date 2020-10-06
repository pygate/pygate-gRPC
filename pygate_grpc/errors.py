import logging
from functools import wraps

import grpc

from pygate_grpc.exceptions import GRPCNotAvailableException, GRPCTimeoutException

logger = logging.getLogger(__name__)


def error_handler(func):
    """A decorator to handle errors"""

    wraps(func)

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except grpc._channel._InactiveRpcError as e:
            err_to_raise = e
            if err_to_raise.code() == grpc.StatusCode.UNAVAILABLE:
                err_to_raise = GRPCNotAvailableException(e)
            # elif err_to_raise.code() == grpc.StatusCode.UNKNOWN:
            #     err_to_raise = PyGateGenericException(e)
        except grpc._channel._MultiThreadedRendezvous as e:
            err_to_raise = e
            if err_to_raise.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                err_to_raise = GRPCTimeoutException(
                    e, e._state, e._call, e._response_deserializer, e._deadline
                )
        raise err_to_raise

    return wrapper


def future_error_handler(func):

    wraps(func)

    def wrapper(*args, **kwargs):
        future = func(*args, **kwargs)
        if hasattr(future, "result") and callable(future.result):
            future.result = error_handler(future.result)
        if hasattr(future, "__next__") and callable(future.__next__):
            future.__next__ = error_handler(future.__next__)
        if hasattr(future, "_next") and callable(future._next):
            future._next = error_handler(future._next)
        return future

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
