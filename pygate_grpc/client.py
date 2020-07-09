from pygate_grpc import health, faults, deals, ffs


class PowerGateClient(object):
    def __init__(self, host_name):
        self.health = health.HealthClient(host_name)
        self.faults = faults.FaultsClient(host_name)
        self.deals = deals.DealsClient(host_name)
        self.ffs = ffs.FfsClient(host_name)


if __name__ == "__main__":
    c = PowerGateClient("127.0.0.1:5002")
    # print()
    # print("creating!", c.ffs.create())
    # print("listing!", c.ffs.listApi())
    # print("addrs list!", c.ffs.addrsList("e795b35b-0c52-4b0d-9791-06334e0c52f0"))
    print("info!", c.ffs.info("QmR74AUggas4mmed9zBAH3NyeeBWzgtDfxidZuxMrLBJw7", "e795b35b-0c52-4b0d-9791-06334e0c52f0"))
    iter = c.ffs.getFileChunks("LICENSE")
    print(iter.__next__())
    # print
    print("info!", c.ffs.addToHot(iter, "e795b35b-0c52-4b0d-9791-06334e0c52f0"))
