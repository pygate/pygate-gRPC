from typing import List
from proto.powergate.v1 import powergate_pb2, powergate_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta


class WalletClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = powergate_pb2_grpc.PowergateServiceStub(channel)
        self.get_metadata = get_metadata

    def balance(self, address, token: str = None):
        req = powergate_pb2.BalanceRequest(address=address)
        return self.client.Balance(req, metadata=self.get_metadata(token))

    # Type should be either `bls` or `secp256k1`.
    def new_address(
        self,
        name: str,
        address_type: str = "bls",
        make_default: bool = false,
        token: str = None,
    ):
        self._check_address_type(address_type)
        req = powergate_pb2.NewAddressRequest(
            name=name, address_type=address_type, make_default=make_default
        )
        return self.client.NewAddress(req, metadata=self.get_metadata(token))

    def addresses(self, token: str = None):
        return self.client.Addresses(
            powergate_pb2.AddressesRequest(), metadata=self.get_metadata(token)
        )

    def send_fil(self, sender: str, receiver: str, amount: str, token: str = None):
        # To avoid name collision since `from` is reserved in Python.
        kwargs = {"from": sender, "to": receiver, "amount": amount}
        req = powergate_pb2.SendFilRequest(**kwargs)
        return self.client.SendFil(req, metadata=self.get_metadata(token))

    def sign_message(self, addr: str, msg: bytes, token: str = None):
        req = powergate_pb2.SignMessageRequest(addr=addr, msg=msg)
        return self.client.SignMessage(req, metadata=self.get_metadata(token))

    def verify_message(
        self, addr: str, msg: bytes, signature: bytes, token: str = None
    ):
        req = powergate_pb2.VerifyMessageRequest(
            addr=addr, msg=msg, signature=signature
        )
        return self.client.VerifyMessage(req, metadata=self.get_metadata(token))

    def _check_address_type(self, wallet_type):
        acceptable_types = ["bls", "secp256k1"]
        if wallet_type not in acceptable_types:
            raise Exception("Type should be one of ", acceptable_types)
