from pygate_grpc.client import PowerGateClient
from pygate_grpc.data import get_file_bytes, bytes_to_chunks


if __name__ == "__main__":

    hostName = "127.0.0.1:5002"

    # Create client
    c = PowerGateClient(hostName, False)

    # Create storage profile
    profile = c.admin.profiles.create_storage_profile()
    print("Profile created:")
    print(profile)

    # Create an iterator of the given file using the helper function
    iter = get_file_bytes("README.md")
    print("Grabbing pygate-grpc 'README.md' file...")
    print("Adding file to IPFS (hot storage)...")

    # Convert the iterator into request and then stage
    res = c.data.stage(bytes_to_chunks(iter), profile.auth_entry.token)
    print(res)
    print("Applying storage config...")

    # Apply the default storage config to the given file
    c.storage_config.apply(res.cid, override=False, token=profile.auth_entry.token)

    # Override push with another config
    addresses = c.wallet.addresses(profile.auth_entry.token)
    wallet = addresses.addresses[0].address
    new_config = (
        '{"hot":{"enabled":true,"allowUnfreeze":true,"ipfs":{"addTimeout":30}},'
        '"cold":{"enabled":true,"filecoin":{"repFactor":1,"dealMinDuration":518400,'
        '"excludedMiners":["t01101"],"trustedMiners":["t01000","t02000"],'
        '"countryCodes":["ca","nl"],"renew":{"enabled":true,"threshold":3},'
        '"addr":"' + wallet + '","maxPrice":50}},"repairable":true}'
    )
    c.storage_config.apply(
        res.cid, override=True, config=new_config, token=profile.auth_entry.token
    )

    # Check that CID is stored
    check = c.data.cid_info([res.cid], profile.auth_entry.token)
    print("Checking CID storage...")
    print(check)

    # Get the data back
    print("Retrieving file " + res.cid)
    file_ = c.data.get(res.cid, profile.auth_entry.token)

    # Write to a file on disk
    print("Saving as 'README_copy.md'")
    with open("README_copy.MD", "wb") as f:
        for f_ in file_:
            f.write(f_)
