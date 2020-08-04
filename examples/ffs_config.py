import json
from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict

client = PowerGateClient("127.0.0.1:5002")

print("Creating a new FFS:")
newFfs = client.ffs.create()
tk = newFfs.token
print("Token: " + tk)
print("Using the new FFS token to request the default config:")
defaultConfig = client.ffs.default_config(tk)
print(defaultConfig)

print("Loading new default config...")
with open("cidconfig.json", "r") as f:
    config = f.read()

client.ffs.set_default_config(config, tk)

defaultConfig = client.ffs.default_config(tk)

print("Updated default config:")
print(json.dumps(MessageToDict(defaultConfig), indent=2))
