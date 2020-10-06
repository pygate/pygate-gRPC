import logging

import proto.wallet_rpc_pb2 as wallet_rpc_pb2
import proto.wallet_rpc_pb2_grpc as wallet_rpc_pb2_grpc

logger = logging.getLogger(__name__)


class WalletClient(object):
    def __init__(self, channel):
        self.client = wallet_rpc_pb2_grpc.RPCServiceStub(channel)

    # Type should be either `bls` or `secp256k1`.
    def list(self, type_="bls"):
        self._check_address_type(type_)
        req = wallet_rpc_pb2.ListRequest(type=type_)
        return self.client.List(req)

    # Type should be either `bls` or `secp256k1`.
    def new(self, type_="bls"):
        self._check_address_type(type_)
        req = wallet_rpc_pb2.NewAddressRequest(type=type_)
        return self.client.NewAddress(req)

    def balance(self, address):
        req = wallet_rpc_pb2.BalanceRequest(address=address)
        return self.client.Balance(req)

    def send_fil(self, sender, receiver, amount):
        kwargs = {"from": sender, "to": receiver, "amount": amount}
        req = wallet_rpc_pb2.SendFilRequest(**kwargs)
        return self.client.SendFil(req)

    def _check_address_type(self, wallet_type):
        acceptable_types = ["bls", "secp256k1"]
        if wallet_type not in acceptable_types:
            raise Exception("Type should be one of ", acceptable_types)
