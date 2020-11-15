import time

from io import BytesIO

from pygate_grpc.client import PowerGateClient
from pygate_grpc.data import bytes_to_chunks

if __name__ == "__main__":

    hostName = "127.0.0.1:5002"

    # Create client
    client = PowerGateClient(hostName)

    # Create user
    user = client.admin.users.create()
    print("User created:")
    print(user)

    print("Applying storage config...")
    stage_res = client.data.stage_bytes(b"These are the contents of a test file", token=user.token)
    apply_res = client.config.apply(stage_res.cid, token=user.token)

    # Check that cid is in the process of being stored by Powegate
    check = client.data.cid_info([stage_res.cid], user.token)
    print("Checking cid storage...")
    print(check)

    # Wait some time so that we can get some deals
    time.sleep(60)

    # Check information about the storage deal
    storage_deals = client.deals.storage_deal_records(
        include_pending=True, include_final=True, token=user.token
    )
    print("Storage deals: ")
    for record in storage_deals:
        print(record)

    # Check information about the retrieval deals
    retrieval_deals = client.deals.retrieval_deal_records(
        include_pending=True, include_final=True, token=user.token
    )
    print("Retrieval deals: ")
    for record in retrieval_deals:
        print(record)
