import os
from pathlib import Path
from pygate_grpc.client import PowerGateClient


if __name__ == "__main__":

    hostName = "127.0.0.1:5002"

    # Create client
    c = PowerGateClient(hostName, False)

    # Create user
    user = c.admin.users.create()
    print("User created:")
    print(user)

    # Stage file
    print("Staging testfile.txt to IPFS storage")
    path = Path(os.path.abspath(__file__))
    staged_file = c.data.stage_file(path.parent / "testfile.txt", user.token)
    print("Applying storage config...")

    # Apply the default storage config to the given file
    c.config.apply(staged_file.cid, override=False, token=user.token)

    # Override push with another config
    addresses = c.wallet.addresses(user.token)
    wallet = addresses[0].address
    new_config = {
        "hot": {"enabled": True, "allowUnfreeze": True, "ipfs": {"addTimeout": 30}},
        "cold": {
            "enabled": True,
            "filecoin": {
                "replicationFactor": 1,
                "dealMinDuration": 518400,
                "excludedMiners": ["t01101"],
                "trustedMiners": ["t01000", "t02000"],
                "countryCodes": ["ca", "nl"],
                "renew": {"enabled": True, "threshold": 3},
                "address": wallet,
                "maxPrice": 50,
            },
        },
        "repairable": True,
    }

    c.config.apply(staged_file.cid, override=True, config=new_config, token=user.token)

    # Check that CID is stored
    check = c.data.cid_info([staged_file.cid], user.token)
    print("Checking CID storage...")
    print(check)

    # Get the data back
    print("Retrieving file " + staged_file.cid)
    file_bytes = c.data.get(staged_file.cid, user.token)

    # Write to a file on disk
    print("Saving as 'testfile_copy.txt'")
    with open(path.parent / "testfile_copy.txt", "wb") as f:
        f.write(file_bytes)
