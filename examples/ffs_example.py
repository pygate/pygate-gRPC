import grpc
from pygate_grpc.client import PowerGateClient


channel = grpc.insecure_channel("127.0.0.1:5002")
client = PowerGateClient(channel)
newFfs = client.ffs.create()
print(newFfs)
