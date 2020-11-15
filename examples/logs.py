from pygate_grpc.client import PowerGateClient
from pygate_grpc.exceptions import GRPCTimeoutException

client = PowerGateClient("127.0.0.1:5002", False)

print("Creating a new user:")
user = client.admin.users.create()
print(user)


stage_res = client.data.stage_bytes(
    b"These are the contents of a test file", user.token
)
apply_res = client.config.apply(stage_res.cid, token=user.token)
logs_res = client.data.watch_logs(stage_res.cid, user.token, history=True, timeout=5)

logs = []
# iterating through the logs is a blocking operation, by using a timeout and
# the following exception handling we can make sure that the operation exits
# after the specified timeout.
try:
    for f in logs_res:
        logs.append(f)
except GRPCTimeoutException:
    pass

print(logs)
