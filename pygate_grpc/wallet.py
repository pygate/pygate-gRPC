from typing import List

from powergate.user.v1 import user_pb2, user_pb2_grpc

from pygate_grpc.decorators import unmarshal_with
from pygate_grpc.errors import ErrorHandlerMeta
from pygate_grpc.types import Address


class WalletClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = user_pb2_grpc.UserServiceStub(channel)
        self.get_metadata = get_metadata

    def balance(self, address, token: str = None) -> int:
        req = user_pb2.BalanceRequest(address=address)
        return int(self.client.Balance(req, metadata=self.get_metadata(token)).balance)

    # Type should be either `bls` or `secp256k1`.
    def new_address(
        self,
        name: str,
        address_type: str = "bls",
        make_default: bool = False,
        token: str = None,
    ):
        self._check_address_type(address_type)
        req = user_pb2.NewAddressRequest(
            name=name, address_type=address_type, make_default=make_default
        )
        return self.client.NewAddress(req, metadata=self.get_metadata(token)).address

    @unmarshal_with(Address, many=True)
    def addresses(self, token: str = None) -> List[Address]:
        return self.client.Addresses(
            user_pb2.AddressesRequest(), metadata=self.get_metadata(token)
        ).addresses

    def send_fil(self, sender: str, receiver: str, amount: str, token: str = None):
        # To avoid name collision since `from` is reserved in Python.
        kwargs = {"from": sender, "to": receiver, "amount": amount}
        req = user_pb2.SendFilRequest(**kwargs)
        return self.client.SendFil(req, metadata=self.get_metadata(token))

    def sign_message(self, addr: str, msg: bytes, token: str = None):
        req = user_pb2.SignMessageRequest(addr=addr, msg=msg)
        return self.client.SignMessage(req, metadata=self.get_metadata(token))

    def verify_message(
        self, addr: str, msg: bytes, signature: bytes, token: str = None
    ):
        req = user_pb2.VerifyMessageRequest(addr=addr, msg=msg, signature=signature)
        return self.client.VerifyMessage(req, metadata=self.get_metadata(token))

    def _check_address_type(self, wallet_type):
        acceptable_types = ["bls", "secp256k1"]
        if wallet_type not in acceptable_types:
            raise Exception("Type should be one of ", acceptable_types)
