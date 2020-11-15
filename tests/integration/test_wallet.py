import logging
import time

import pytest

from pygate_grpc.client import PowerGateClient
from pygate_grpc.types import Address, User

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def user(pygate_client: PowerGateClient):
    return pygate_client.admin.users.create()


def test_wallet_list(pygate_client: PowerGateClient, user: User):
    addresses = pygate_client.wallet.addresses(user.token)

    assert addresses is not None
    assert len(addresses) >= 1
    assert type(addresses[0]) == Address


def test_wallet_new(pygate_client: PowerGateClient, user: User):
    addr_name = "Test Address"
    addr_type = "secp256k1"
    address = pygate_client.wallet.new_address(
        name=addr_name, address_type=addr_type, token=user.token
    )

    assert address is not None
    assert type(address) == str

    address_details = next(
        addr
        for addr in pygate_client.wallet.addresses(token=user.token)
        if addr.address == address
    )
    assert address_details.name == addr_name
    assert address_details.type == addr_type


def test_wallet_balance(pygate_client: PowerGateClient, user: User):
    user_addr = pygate_client.wallet.addresses(user.token)[0].address

    timeout = 5
    start = int(time.time())
    balance = pygate_client.wallet.balance(user_addr)
    while balance != 250000000000000000:
        time.sleep(1)
        balance = pygate_client.wallet.balance(user_addr)
        now = int(time.time())
        if now - start > timeout:
            raise Exception("Waiting for wallet to initialize timed out")

    assert type(balance) is int
    assert balance == 250000000000000000
