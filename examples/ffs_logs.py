import time

from io import BytesIO

from pygate_grpc.client import PowerGateClient
from pygate_grpc.ffs import bytes_to_chunks
from pygate_grpc.exceptions import GRPCTimeoutException
from pygate_grpc.errors import error_handler

client = PowerGateClient("127.0.0.1:5002", False)

print("Creating a new FFS:")
ffs = client.ffs.create()
print(ffs)

test_file = BytesIO(b"These are the contents of a test file")
stage_requests_iter = bytes_to_chunks(test_file)

stage_res = client.ffs.stage(stage_requests_iter, ffs.token)
push_res = client.ffs.push(stage_res.cid, ffs.token)
logs_res = client.ffs.logs(stage_res.cid, ffs.token, history=True, timeout=5)

logs=[]
# iterating through the logs is a blocking operation, by using a timeout and
# the following exception handling we can make sure that the operation exits
# after the specified timeout.
try:
    for f in logs_res:
        logs.append(f)
except GRPCTimeoutException:
    pass

print(logs)
