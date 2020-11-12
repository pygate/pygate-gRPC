import time

from io import BytesIO

from pygate_grpc.client import PowerGateClient
from pygate_grpc.data import bytes_to_chunks

if __name__ == "__main__":

    hostName = "127.0.0.1:5002"

    # Create client
    client = PowerGateClient(hostName)

    # Create user
    res = client.admin.users.create()
    print("User created:")
    print(res)

    test_file = BytesIO(b"These are the contents of a test file")
    stage_requests_iter = bytes_to_chunks(test_file)

    print("Applying storage config...")
    stage_res = client.data.stage(stage_requests_iter, token=res.user.token)
    apply_res = client.storage_config.apply(stage_res.cid, token=res.user.token)

    # Check that cid is in the process of being stored by Powegate
    check = client.data.cid_info([stage_res.cid], res.user.token)
    print("Checking cid storage...")
    print(check)

    # Wait some time so that we can get some deals
    time.sleep(60)

    # Check information about the storage deal
    storage_deals = client.deals.storage_deal_records(
        include_pending=True, include_final=True, token=res.user.token
    )
    print("Storage deals: ")
    for record in storage_deals.records:
        print(record)

    # Check information about the retrieval deals
    retrieval_deals = client.deals.retrieval_deal_records(
        include_pending=True, include_final=True, token=res.user.token
    )
    print("Retrieval deals: ")
    for record in retrieval_deals.records:
        print(record)
