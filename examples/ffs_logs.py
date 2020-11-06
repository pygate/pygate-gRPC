from io import BytesIO

from pygate_grpc.client import PowerGateClient
from pygate_grpc.data import bytes_to_chunks
from pygate_grpc.exceptions import GRPCTimeoutException

client = PowerGateClient("127.0.0.1:5002", False)

print("Creating a new storage profile:")
profile = client.admin.profiles.create_storage_profile()
print(profile)

test_file = BytesIO(b"These are the contents of a test file")
stage_requests_iter = bytes_to_chunks(test_file)

stage_res = client.data.stage(stage_requests_iter, profile.auth_entry.token)
apply_res = client.storage_config.apply(stage_res.cid, token=profile.auth_entry.token)
logs_res = client.data.watch_logs(
    stage_res.cid, profile.auth_entry.token, history=True, timeout=5
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
