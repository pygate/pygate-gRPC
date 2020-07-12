class GRPCNotAvailableException(Exception):
    def __init__(self, err, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_err = err
