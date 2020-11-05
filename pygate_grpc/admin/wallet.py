from proto.admin.v1 import powergate_admin_pb2, powergate_admin_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta


class WalletClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = powergate_admin_pb2_grpc.PowergateAdminServiceStub(channel)
        self.get_metadata = get_metadata

    # Type should be either `bls` or `secp256k1`.
    def new_address(
        self,
        address_type: str = "bls",
        admin_token: str = None,
    ):
        self._check_address_type(address_type)
        req = powergate_admin_pb2.NewAddressRequest(address_type=address_type)
        return self.client.NewAddress(req, metadata=self.get_metadata(admin_token))

    def addresses(self, admin_token: str = None):
        return self.client.Addresses(
            powergate_admin_pb2.AddressesRequest(),
            metadata=self.get_metadata(admin_token),
        )

    def send_fil(
        self, sender: str, receiver: str, amount: str, admin_token: str = None
    ):
        # To avoid name collision since `from` is reserved in Python.
        kwargs = {"from": sender, "to": receiver, "amount": amount}
        req = powergate_admin_pb2.SendFilRequest(**kwargs)
        return self.client.SendFil(req, metadata=self.get_metadata(admin_token))

    def _check_address_type(self, wallet_type):
        acceptable_types = ["bls", "secp256k1"]
        if wallet_type not in acceptable_types:
            raise Exception("Type should be one of ", acceptable_types)
