from pygate_grpc.client import PowerGateClient

client = PowerGateClient("127.0.0.1:5002", False)

build_info = client.build_info()
print(build_info)

user = client.admin.users.create()

user_id = client.user_id(user.token)
print(user_id)
