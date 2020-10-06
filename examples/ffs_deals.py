import time

from io import BytesIO

from pygate_grpc.client import PowerGateClient
from pygate_grpc.ffs import bytes_to_chunks

if __name__ == "__main__":

    hostName = "127.0.0.1:5002"

    # Create client
    client = PowerGateClient(hostName)

    # Create FFS
    ffs = client.ffs.create()
    print("FFS created:")
    print(ffs)

    test_file = BytesIO(b"These are the contents of a test file")
    stage_requests_iter = bytes_to_chunks(test_file)

    print("Pushing file to FFS...")
    stage_res = client.ffs.stage(stage_requests_iter, token=ffs.token)
    push_res = client.ffs.push(stage_res.cid, token=ffs.token)

    # Check that CID is pinned to FFS
    check = client.ffs.info(stage_res.cid, ffs.token)
    print("Checking FFS pins...")
    print(check)

    # Wait some time so that we can get some deals
    time.sleep(5)

    # Check information about the storage deal
    storage_deals = client.ffs.list_storage_deal_records(
        include_pending=True, include_final=True, token=ffs.token
    )
    print("Storage deals: ")
    for record in storage_deals.records:
        print(record)

    # Check information about the retrieval deals
    retrieval_deals = client.ffs.list_retrieval_deal_records(
        include_pending=True, include_final=True, token=ffs.token
    )
    print("Retrieval deals: ")
    for record in retrieval_deals.records:
        print(record)
