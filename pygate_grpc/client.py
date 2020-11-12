import grpc
from typing import Tuple
from powergate.user.v1 import user_pb2, user_pb2_grpc
from pygate_grpc import data, deals, storage_config, storage_jobs, wallet
from pygate_grpc.admin import admin
from pygate_grpc.errors import ErrorHandlerMeta

TOKEN_KEY = "x-ffs-token"
ADMIN_TOKEN_KEY = "X-pow-admin-token"


class PowerGateClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, host_name, is_secure=False):
        channel = (
            grpc.secure_channel(host_name, grpc.ssl_channel_credentials())
            if is_secure
            else grpc.insecure_channel(host_name)
        )
        self.client = user_pb2_grpc.UserServiceStub(channel)

        self.token = None
        self.admin_token = None

        self.admin = admin.AdminClient(channel, self.get_metadata)
        self.data = data.DataClient(channel, self.get_metadata)
        self.deals = deals.DealsClient(channel, self.get_metadata)
        self.storage_config = storage_config.StorageConfigClient(
            channel, self.get_metadata
        )
        self.storage_jobs = storage_jobs.StorageJobsClient(channel, self.get_metadata)
        self.wallet = wallet.WalletClient(channel, self.get_metadata)

    def set_token(self, token: str):
        self.token = token

    def set_admin_token(self, token: str):
        self.admin_token = token

    def build_info(self):
        req = user_pb2.BuildInfoRequest()
        return self.client.BuildInfo(req)

    def user_id(self, token: str = None):
        req = user_pb2.UserIdentifierRequest()
        return self.client.UserIdentifier(req, metadata=self.get_metadata(token))

    # The metadata is set in here https://github.com/textileio/js-powergate-client/blob
    # /9d1ad04a7e1f2a6e18cc5627751f9cbddaf6fe05/src/util/grpc-helpers.ts#L7 Note that you can't have capital letter in
    # meta data field, see here: https://stackoverflow.com/questions/45071567/how-to-send-custom-header-metadata-with
    # -python-grpc
    def get_metadata(
        self, token: str = None, admin_token: str = None
    ) -> Tuple[Tuple[str, str]]:
        token_data: Tuple[Tuple[str, str]] = ()
        admin_token_data: Tuple[Tuple[str, str]] = ()

        final_token = token if token else self.token
        final_admin_token = admin_token if admin_token else self.admin_token

        if final_token is not None:
            token_data = ((TOKEN_KEY, final_token),)
        if final_admin_token is not None:
            admin_token_data = ((ADMIN_TOKEN_KEY, final_admin_token),)

        return token_data + admin_token_data
