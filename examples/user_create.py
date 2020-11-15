from pygate_grpc.client import PowerGateClient

client = PowerGateClient("127.0.0.1:5002", False)

print("Creating a new user:")
new_user = client.admin.users.create()
print(new_user)
