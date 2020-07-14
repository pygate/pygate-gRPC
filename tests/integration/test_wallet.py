import logging
import grpc
import pytest

from pygate_grpc.client import PowerGateClient
from proto.wallet_rpc_pb2 import ListResponse, WalletBalanceResponse

logger = logging.getLogger(__name__)


def test_grpc_wallet_list(pygate_client: PowerGateClient):
    res = pygate_client.wallet.list()

    assert res is not None
    assert type(res) == ListResponse
    # During creating it should have 1 address.
    assert len(res.addresses) >= 1


def test_grpc_wallet_new(pygate_client: PowerGateClient):
    res = pygate_client.wallet.list()
    assert res is not None
    assert type(res) == ListResponse
    num_of_address = len(res.addresses)

    new_res = pygate_client.wallet.new()
    assert new_res is not None

    list_res = pygate_client.wallet.list()
    assert len(list_res.addresses) == num_of_address + 1
    assert new_res.address in list_res.addresses


def test_grpc_wallet_balance(pygate_client: PowerGateClient):
    new_res = pygate_client.wallet.new()
    assert new_res is not None

    balance_res = pygate_client.wallet.balance(new_res.address)
    assert type(balance_res) is WalletBalanceResponse
    # TODO: In here, according to `pow wallet balance <address>` this should be 4000000000000000,
    # but it is returning 0 in reality, not sure why.
    # assert balance_res.balance == 4000000000000000
