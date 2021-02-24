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
    print("Staging 'testfile.txt' to IPFS storage...")
    path = Path(os.path.abspath(__file__))
    staged_file = c.data.stage_file(path.parent / "testfile.txt", user.token)
    print("IPFS CID: " + staged_file.cid)

    # Apply the default storage config to the given file
    print("Applying Filecoin storage config to CID...")
    job = c.config.apply(staged_file.cid, override=False, token=user.token)

    # Report back the Job ID for the successful Filecoin storage job
    print("File successfully added to Filecoin storage.")
    print("Job ID: " + job.jobId)

    storage_infos = c.storage_info.list(cids=[staged_file.cid], token=user.token)
    print(storage_infos)
