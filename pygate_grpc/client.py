import health
import faults
import deals

class PowerGateClient(object):
    def __init__(self, hostName):
        self.health = health.HealthClient(hostName)
        self.faults = faults.FaultsClient(hostName)
        self.deals = deals.DealsClient(hostName)


if __name__ == "__main__":
    c = PowerGateClient("127.0.0.1:5002")
    print(c.faults.get())