from pygate_grpc.client import PowerGateClient

client = PowerGateClient("127.0.0.1:5002", False)

print("Creating a new storage profile:")
new_profile = client.admin.profiles.create_storage_profile()
tk = new_profile.auth_entry.token
print("Token: " + tk)
print("Using the new profile token to request the default config:")
defaultConfig = client.storage_config.default(tk)
print(defaultConfig)

print("Loading new default config...")
with open("cidconfig.json", "r") as f:
    config = f.read()

client.storage_config.set_default(config, tk)

defaultConfig = client.storage_config.default(tk)
print("Updated default config:")
print(defaultConfig)
