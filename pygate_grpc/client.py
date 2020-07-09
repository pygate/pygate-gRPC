from pygate_grpc import health, faults, deals, ffs


class PowerGateClient(object):
    def __init__(self, hostName):
        self.health = health.HealthClient(hostName)
        self.faults = faults.FaultsClient(hostName)
        self.deals = deals.DealsClient(hostName)
        self.ffs = ffs.FfsClient(hostName)


# if __name__ == "__main__":
#     c = PowerGateClient("127.0.0.1:5002")
#     # print()
#     # print("creating!", c.ffs.create())
#     # print("listing!", c.ffs.listApi())
#     # print("addrs list!", c.ffs.addrsList("e795b35b-0c52-4b0d-9791-06334e0c52f0"))
#     print(
#         "info!",
#         c.ffs.info(
#             "QmR74AUggas4mmed9zBAH3NyeeBWzgtDfxidZuxMrLBJw7",
#             "e795b35b-0c52-4b0d-9791-06334e0c52f0",
#         ),
#     )
