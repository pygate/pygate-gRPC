import grpc

from pygate_grpc import buildinfo, faults, ffs, health, net, wallet
from pygate_grpc.errors import ErrorHandlerMeta


class PowerGateClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, host_name, is_secure=False):
        self.channel = (
            grpc.secure_channel(host_name, grpc.ssl_channel_credentials())
            if is_secure
            else grpc.insecure_channel(host_name)
        )

        self.health = health.HealthClient(self.channel)
        self.faults = faults.FaultsClient(self.channel)
        self.buildinfo = buildinfo.BuildinfoClient(self.channel)
        self.ffs = ffs.FfsClient(self.channel)
        self.wallet = wallet.WalletClient(self.channel)
        self.net = net.NetClient(self.channel)
