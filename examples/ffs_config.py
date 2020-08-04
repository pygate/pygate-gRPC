from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import Parse
from proto.ffs_rpc_pb2 import StorageConfig

client = PowerGateClient("127.0.0.1:5002")

print("Creating a new FFS:")
newFfs = client.ffs.create()
tk = newFfs.token
print("Token: " + tk)
print("Using the new FFS token to request the default config:")
defaultConfig = client.ffs.default_config(tk)
newConfig = """
{
  "hot": {
    "enabled": true,
    "ipfs": {
      "add_timeout": "30"
    }
  },
  "cold": {
    "enabled": true,
    "filecoin": {
      "rep_factor": "1",
      "deal_min_duration": "1000",
      "renew": {},
      "addr": "t3uubebjuye33jwzova3zyxrxgan37p3wjeaxfe5xml2utcqbyku67zujh46na2wgbvzgblgi4sgbqtu4b6t6a"
    }
  },
  "repairable": true
}
"""

client.ffs.set_default_config(Parse(newConfig, StorageConfig()), tk)
defaultConfig = client.ffs.default_config(tk)
print(defaultConfig)
