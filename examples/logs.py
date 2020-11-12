from io import BytesIO

from pygate_grpc.client import PowerGateClient
from pygate_grpc.data import bytes_to_chunks
from pygate_grpc.exceptions import GRPCTimeoutException

client = PowerGateClient("127.0.0.1:5002", False)

print("Creating a new user:")
res = client.admin.users.create()
print(res)

test_file = BytesIO(b"These are the contents of a test file")
stage_requests_iter = bytes_to_chunks(test_file)

stage_res = client.data.stage(stage_requests_iter, res.user.token)
apply_res = client.storage_config.apply(stage_res.cid, token=res.user.token)
logs_res = client.data.watch_logs(
    stage_res.cid, res.user.token, history=True, timeout=5
)

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
