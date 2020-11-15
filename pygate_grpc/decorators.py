from functools import wraps

from google.protobuf.json_format import MessageToDict


def unmarshal_with(cls=None, many=False):
    """
    Unmarshals the protobuf response result to the given object
    """

    def wrap(original_func):

        wraps(original_func)

        def wrapper(*args, **kwargs):
            if cls is None:
                if many:

                    return [
                        MessageToDict(obj) for obj in original_func(*args, **kwargs)
                    ]
                return MessageToDict(original_func(*args, **kwargs))
            else:
                if many:
                    return [
                        cls(**MessageToDict(obj))
                        for obj in original_func(*args, **kwargs)
                    ]
                return cls(**MessageToDict(original_func(*args, **kwargs)))

        return wrapper

    return wrap
