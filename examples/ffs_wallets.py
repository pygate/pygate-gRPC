from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToJson
import json

client = PowerGateClient("127.0.0.1:5002")

print("Creating a new FFS:")
newFfs = client.ffs.create()
print(newFfs)

wallet = client.ffs.addrs_list(newFfs.token)

print("Wallet address:")
print(wallet)

jsonObj = MessageToJson(wallet)
#print(j)
info = json.loads(jsonObj)
print(info['addrs'][0]['addr'])

print("wallet type:")
print(type(wallet))


