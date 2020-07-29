from pygate_grpc.client import PowerGateClient

client = PowerGateClient("127.0.0.1:5002")

print("Creating a new FFS:")
newFfs = client.ffs.create()
tk = newFfs.token
print("Token: " + tk)
print("Using the new FFS token to request the default config:")
defaultConfig = client.ffs.default_config(tk)
print(defaultConfig)
