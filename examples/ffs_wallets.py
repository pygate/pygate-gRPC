from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict


client = PowerGateClient("127.0.0.1:5002")

print("Creating a new FFS:")
newFfs = client.ffs.create()
print(newFfs)

wallet = client.ffs.addrs_list(newFfs.token)
obj = MessageToDict(wallet)

print(obj['addrs'][0]['addr'])

print("wallet type:")
print(type(wallet))
print(type(obj))


