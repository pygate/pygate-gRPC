import logging

from pygate_grpc.client import PowerGateClient
from proto.wallet_rpc_pb2 import ListResponse, BalanceResponse
import time

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

    # Wait a bit for the transaction to finish.
    time.sleep(5)

    balance_res = pygate_client.wallet.balance(new_res.address)
    assert type(balance_res) is BalanceResponse
    assert balance_res.balance == 4000000000000000


def test_send_file(pygate_client: PowerGateClient):
    addr = pygate_client.wallet.new()

    assert addr is not None
    assert addr.address is not None

    res = pygate_client.wallet.list()

    assert res is not None

    sender_addr = res.addresses[0]
    receiver_addr = res.addresses[1]

    before_sender_fil = pygate_client.wallet.balance(sender_addr)
    before_receiver_fil = pygate_client.wallet.balance(receiver_addr)

    pygate_client.wallet.send_fil(sender_addr, receiver_addr, 1)

    # Wait a bit for transaction to complete
    time.sleep(5)
    after_sender_fil = pygate_client.wallet.balance(sender_addr)
    after_receiver_fil = pygate_client.wallet.balance(receiver_addr)

    assert (before_sender_fil.balance - 1) == after_sender_fil.balance
    assert (before_receiver_fil.balance + 1) == after_receiver_fil.balance
