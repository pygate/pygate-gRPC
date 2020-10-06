from grpc._channel import _MultiThreadedRendezvous


class GRPCNotAvailableException(Exception):
    def __init__(self, err, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_err = err


class GRPCTimeoutException(_MultiThreadedRendezvous):
    def __init__(self, err, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_err = err


class PyGateGenericException(Exception):
    def __init__(self, err, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_err = err

        def __repr__(self):
            return self.original_err.__repr__()

        def __str__(self):
            return self.original_err.__str__()
