from pygate_grpc.client import PowerGateClient

client = PowerGateClient("127.0.0.1:5002")

print("Creating a new FFS:")
newFfs = client.ffs.create()
print(newFfs)
