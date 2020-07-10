import proto.ffs_rpc_pb2 as ffs_rpc_pb2
from pygate_grpc import health, faults, deals, ffs

class PowerGateClient(object):
    def __init__(self, host_name):
        self.health = health.HealthClient(host_name)
        self.faults = faults.FaultsClient(host_name)
        self.deals = deals.DealsClient(host_name)
        self.ffs = ffs.FfsClient(host_name)


if __name__ == "__main__":
    pass
