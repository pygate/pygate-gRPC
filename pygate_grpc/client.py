import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import proto.ffs_rpc_pb2 as ffs_rpc_pb2
from pygate_grpc import health, faults, deals, ffs

class PowerGateClient(object):
    def __init__(self, host_name):
        self.health = health.HealthClient(host_name)
        self.faults = faults.FaultsClient(host_name)
        self.deals = deals.DealsClient(host_name)
        self.ffs = ffs.FfsClient(host_name)


if __name__ == "__main__":
    c = PowerGateClient("127.0.0.1:5002")
    iter = c.ffs.get_file_bytes("README.md")
    res = c.ffs.add_to_hot(c.ffs.bytes_to_chunks(iter), "e795b35b-0c52-4b0d-9791-06334e0c52f0")
    print("res", res.cid)
    c.ffs.push(res.cid, "e795b35b-0c52-4b0d-9791-06334e0c52f0")
    bs = c.ffs.get(res.cid, "e795b35b-0c52-4b0d-9791-06334e0c52f0")
    print("bs", next(bs))
