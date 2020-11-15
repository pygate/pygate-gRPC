from typing import List

from powergate.admin.v1 import admin_pb2, admin_pb2_grpc

from pygate_grpc.errors import ErrorHandlerMeta


class WalletClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = admin_pb2_grpc.AdminServiceStub(channel)
        self.get_metadata = get_metadata

    # Type should be either `bls` or `secp256k1`.
    def new(self, address_type: str = "bls", admin_token: str = None,) -> str:
        self._check_address_type(address_type)
        req = admin_pb2.NewAddressRequest(address_type=address_type)
        return self.client.NewAddress(
            req, metadata=self.get_metadata(admin_token)
        ).address

    def addresses(self, admin_token: str = None) -> List[str]:
        return list(
            self.client.Addresses(
                admin_pb2.AddressesRequest(), metadata=self.get_metadata(admin_token),
            ).addresses
        )

    def send(self, sender: str, receiver: str, amount: int, admin_token: str = None):
        if type(amount) == float:
            raise TypeError("amount should be an integer")
        # To avoid name collision since `from` is reserved in Python.
        kwargs = {"from": sender, "to": receiver, "amount": str(amount)}
        req = admin_pb2.SendFilRequest(**kwargs)
        return self.client.SendFil(req, metadata=self.get_metadata(admin_token))

    def _check_address_type(self, wallet_type):
        acceptable_types = ["bls", "secp256k1"]
        if wallet_type not in acceptable_types:
            raise Exception("Type should be one of ", acceptable_types)
