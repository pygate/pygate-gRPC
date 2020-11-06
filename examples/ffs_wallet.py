import time
from pygate_grpc.client import PowerGateClient


client = PowerGateClient("127.0.0.1:5002", False)

all_addresses = client.admin.wallet.addresses()
print("All addresses:")
print(all_addresses)


print("Creating a new storage profile:")
profile = client.admin.profiles.create_storage_profile()
print(profile)

addresses = client.wallet.addresses(profile.auth_entry.token)
address = addresses.addresses[0].address
print("Profile wallet address: " + address)

print("Waiting for wallet to get funding...")
time.sleep(2)

balance = client.wallet.balance(address)
print("Wallet balance: ", str(balance.balance))
