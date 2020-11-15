from typing import Tuple

import grpc
from powergate.user.v1 import user_pb2, user_pb2_grpc

from pygate_grpc.admin import AdminClient
from pygate_grpc.config import ConfigClient
from pygate_grpc.data import DataClient
from pygate_grpc.deals import DealsClient
from pygate_grpc.decorators import unmarshal_with
from pygate_grpc.errors import ErrorHandlerMeta
from pygate_grpc.storage_jobs import StorageJobsClient
from pygate_grpc.types import BuildInfo
from pygate_grpc.wallet import WalletClient

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

        self.admin = AdminClient(channel, self.get_metadata)
        self.data = DataClient(channel, self.get_metadata)
        self.deals = DealsClient(channel, self.get_metadata)
        self.config = ConfigClient(channel, self.get_metadata)
        self.storage_jobs = StorageJobsClient(channel, self.get_metadata)
        self.wallet = WalletClient(channel, self.get_metadata)

    def set_token(self, token: str):
        self.token = token

    def set_admin_token(self, token: str):
        self.admin_token = token

    @unmarshal_with(BuildInfo)
    def build_info(self) -> BuildInfo:
        req = user_pb2.BuildInfoRequest()
        return self.client.BuildInfo(req)

    def user_id(self, token: str = None) -> str:
        req = user_pb2.UserIdentifierRequest()
        return self.client.UserIdentifier(req, metadata=self.get_metadata(token)).id

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
