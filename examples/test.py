import time

from pygate_grpc.client import PowerGateClient

client = PowerGateClient("127.0.0.1:5002", False)

print("Creating a new user:")
user = client.admin.users.create()
print(user)


staged_file = client.data.stage_bytes(b"Some random bytes", token=user.token)


client.config.apply(staged_file.cid, token=user.token)

time.sleep(3)

storage_deals = client.deals.storage_deal_records(
    include_pending=True, include_final=True, token=user.token
)

ret_deals = client.deals.retrieval_deal_records(
    include_pending=True, include_final=True, token=user.token
)
