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
    iter = get_file_bytes("pygate-concept-v2.png")
    print("Grabbing pygate-grpc 'README.md' file...")
    print("Adding file to IPFS (hot storage)...")

    # Convert the iterator into request and then add to hot set
    res = c.ffs.add_to_hot(bytes_to_chunks(iter), ffs.token)
    print(res)
    print("Pushing file to FFS...")

    # Push the given file
    c.ffs.push(res.cid, ffs.token)

    # Check that CID is pinned to FFS
    check = c.ffs.info(res.cid, ffs.token)
    print("Checking FFS pins...")
    print(check)

    # Get the file back
    file_ = c.ffs.get(res.cid, ffs.token)
    print("Retrieving file " + res.cid + " from FFS:")
    # print(next(file))

    f = open("pygate-concept-v2-copy.png", "wb")
    f.write(next(file_))
    f.close()
