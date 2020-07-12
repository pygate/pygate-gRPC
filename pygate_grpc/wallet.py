import grpc
import logging
import proto.wallet_rpc_pb2 as wallet_rpc_pb2
import proto.wallet_rpc_pb2_grpc as wallet_rpc_pb2_grpc

logger = logging.getLogger(__name__)


class WalletClient(object):
    def __init__(self, host_name):
        channel = grpc.insecure_channel(host_name)
        self.client = wallet_rpc_pb2_grpc.RPCServiceStub(channel)

    # Type should be either `bls` or `secp256k1`.
    def list(self, type_="bls"):
        req = wallet_rpc_pb2.ListRequest(type=type_)
        return self.client.List(req)

    # Type should be either `bls` or `secp256k1`.
    def new(self, type_="bls"):
        req = wallet_rpc_pb2.NewAddressRequest(type=type_)
        return self.client.NewAddress(req)

    def balance(self, address):
        req = wallet_rpc_pb2.WalletBalanceRequest(address=address)
        return self.client.WalletBalance(req)
