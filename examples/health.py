from pygate_grpc.client import PowerGateClient

client = PowerGateClient("127.0.0.1:5002", False)

print("Checking node health...")
healthcheck = client.health.check()
print(healthcheck)
