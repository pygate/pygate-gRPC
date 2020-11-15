import time
from pygate_grpc.client import PowerGateClient


client = PowerGateClient("127.0.0.1:5002", False)

all_addresses = client.admin.wallet.addresses()
print("All addresses:")
print(all_addresses)


print("Creating a new user:")
user = client.admin.users.create()
print(user)

addresses = client.wallet.addresses(user.token)
address = addresses[0].address
print("User wallet address: " + address)

print("Waiting for wallet to get funding...")
time.sleep(2)

balance = client.wallet.balance(address)
print("Wallet balance: ", str(balance))
