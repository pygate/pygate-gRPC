from pygate_grpc.client import PowerGateClient
from pygate_grpc.data import get_file_bytes, byte_chunks_iter

import os
import json
from pathlib import Path


client = PowerGateClient("127.0.0.1:5002", False)

print("Creating a new user:")
user = client.admin.users.create()
tk = user.token
print("Token: " + tk)
print("Using the new user token to request the default config:")
default_config = client.config.default(tk)

wallets = client.wallet.addresses(token=tk)
print("Addresses: {0}".format(default_config))

print("Loading new default config...")
path = Path(os.path.abspath(__file__))
with open(path.parent / "cidconfig_example.json", "r") as f:
    config = json.load(f)
config["cold"]["filecoin"]["address"] = wallets[0].address

client.config.set_default(config, tk)

default_config = client.config.default(tk)
print("Updated default config:")
print(default_config)

test_bytes = b"These are some test bytes"
staged_file = client.data.stage_bytes(test_bytes, user.token)
print("StagedFile: ", staged_file)

job = client.config.apply(staged_file.cid, token=user.token, config=config)
print(job)

file_bytes = client.data.get(staged_file.cid, token=user.token)
print(file_bytes)
