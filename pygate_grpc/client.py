from proto import ffs_rpc_pb2
from pygate_grpc import health, faults, buildinfo, ffs, wallet, net


class PowerGateClient(object):
    def __init__(self, host_name, is_secure):
        self.health = health.HealthClient(host_name, is_secure)
        self.faults = faults.FaultsClient(host_name, is_secure)
        self.buildinfo = buildinfo.BuildinfoClient(host_name, is_secure)
        self.ffs = ffs.FfsClient(host_name, is_secure)
        self.wallet = wallet.WalletClient(host_name, is_secure)
        self.net = net.NetClient(host_name, is_secure)
