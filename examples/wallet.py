import time
from pygate_grpc.client import PowerGateClient


client = PowerGateClient("127.0.0.1:5002", False)

all_addresses = client.admin.wallet.addresses()
print("All addresses:")
print(all_addresses)


print("Creating a new user:")
res = client.admin.users.create()
print(res)

addresses = client.wallet.addresses(res.user.token)
address = addresses.addresses[0].address
print("User wallet address: " + address)

print("Waiting for wallet to get funding...")
time.sleep(2)

balance = client.wallet.balance(address)
print("Wallet balance: ", str(balance.balance))
