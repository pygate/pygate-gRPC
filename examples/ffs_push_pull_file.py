from pygate_grpc.client import PowerGateClient
from pygate_grpc.ffs import get_file_bytes, bytes_to_chunks


if __name__ == "__main__":

    hostName = "127.0.0.1:5002"

    # Create client
    c = PowerGateClient(hostName, False)

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
    c.ffs.push(res.cid, override=False, token=ffs.token)
    # Override push with another config
    addresses = c.ffs.addrs_list(ffs.token)
    wallet = addresses.addrs[0].addr
    new_config = (
        '{"hot":{"enabled":true,"allowUnfreeze":true,"ipfs":{"addTimeout":30}},'
        '"cold":{"enabled":true,"filecoin":{"repFactor":1,"dealMinDuration":518400,'
        '"excludedMiners":["t01101"],"trustedMiners":["t01000","t02000"],'
        '"countryCodes":["ca","nl"],"renew":{"enabled":true,"threshold":3},'
        '"addr":"' + wallet + '","maxPrice":50}},"repairable":true}'
    )
    c.ffs.push(res.cid, override=True, config=new_config, token=ffs.token)

    # Check that CID is pinned to FFS
    check = c.ffs.info(res.cid, ffs.token)
    print("Checking FFS pins...")
    print(check)

    # Get the data back
    print("Retrieving file " + res.cid + " from FFS.")
    file_ = c.ffs.get(res.cid, ffs.token)

    # Write to a file on disk
    print("Saving as 'README_copy.md'")
    with open("README_copy.MD", "wb") as f:
        for f_ in file_:
            f.write(f_)
