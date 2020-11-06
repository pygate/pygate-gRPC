from pygate_grpc.client import PowerGateClient

client = PowerGateClient("127.0.0.1:5002", False)

print("Creating a new storage profile:")
new_profile = client.admin.profiles.create_storage_profile()
print(new_profile)
