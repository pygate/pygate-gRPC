from pygate_grpc.admin import storage_jobs, users, wallet
from pygate_grpc.errors import ErrorHandlerMeta


class AdminClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.users = users.UsersClient(channel, get_metadata)
        self.storage_jobs = storage_jobs.StorageJobsClient(channel, get_metadata)
        self.wallet = wallet.WalletClient(channel, get_metadata)
