from pygate_grpc.client import PowerGateClient
from pygate_grpc.ffs import get_file_bytes, bytes_to_chunks


if __name__ == "__main__":

    hostName = "127.0.0.1:5002"

    # Create client
    c = PowerGateClient(hostName)

    # Create FFS
    ffs = c.ffs.create()
    print("FFS created:")
    print(ffs)

    # Create an iterator of the given file using the helper function
    iter = get_file_bytes("README.md")
    print("Grabbing pygate-grpc 'README.md' file...")
    print("Adding file to IPFS (hot storage)...")

    # Convert the iterator into request and then add to hot set
    res = c.ffs.stage(bytes_to_chunks(iter), ffs.token)
    print(res)
    print("Pushing file to FFS...")

    # Push the given file
    c.ffs.push(res.cid, ffs.token)

    # Check that CID is pinned to FFS
    check = c.ffs.info(res.cid, ffs.token)
    print("Checking FFS pins...")
    print(check)

    # Check information about the storage deal
    deals = c.ffs.list_storage_deal_records(ffs.token)
    for deal in deals:
        print(deal)
