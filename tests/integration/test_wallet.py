import logging
import time

from powergate.admin.v1.admin_pb2 import AddressesResponse
from powergate.user.v1.user_pb2 import BalanceResponse
from pygate_grpc.client import PowerGateClient

logger = logging.getLogger(__name__)


def test_grpc_wallet_list(pygate_client: PowerGateClient):
    res = pygate_client.admin.wallet.addresses()

    assert res is not None
    assert type(res) == AddressesResponse
    # During creating it should have 1 address.
    assert len(res.addresses) >= 1


def test_grpc_wallet_new(pygate_client: PowerGateClient):
    res = pygate_client.admin.wallet.addresses()
    assert res is not None
    assert type(res) == AddressesResponse
    num_of_address = len(res.addresses)

    new_res = pygate_client.admin.wallet.new_address()
    assert new_res is not None

    list_res = pygate_client.admin.wallet.addresses()
    assert len(list_res.addresses) == num_of_address + 1
    assert new_res.address in list_res.addresses


def test_grpc_wallet_balance(pygate_client: PowerGateClient):
    new_res = pygate_client.admin.wallet.new_address()
    assert new_res is not None

    # Wait a bit for the transaction to finish.
    time.sleep(5)

    balance_res = pygate_client.wallet.balance(new_res.address)
    assert type(balance_res) is BalanceResponse
    assert balance_res.balance == 250000000000000000
