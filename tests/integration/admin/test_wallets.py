import logging
import time

import pytest

from pygate_grpc.client import PowerGateClient

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def wallets(pygate_client: PowerGateClient):
    wallet1 = pygate_client.admin.wallet.new()
    wallet2 = pygate_client.admin.wallet.new()
    return wallet1, wallet2


def test_grpc_wallet_create(pygate_client: PowerGateClient):
    wallet_addr = pygate_client.admin.wallet.new()

    assert type(wallet_addr) == str
    assert len(wallet_addr) > 0


def test_grpc_wallet_list(pygate_client: PowerGateClient, wallets: tuple):
    wallet_addrs = pygate_client.admin.wallet.addresses()

    assert type(wallet_addrs) == list
    assert len(wallet_addrs) > 1
    assert wallets[0] in wallet_addrs
    assert wallets[1] in wallet_addrs


def test_grpc_wallet_send(pygate_client: PowerGateClient, wallets: tuple):
    sender = wallets[0]
    receiver = wallets[1]
    # Wait until wallets are initialized
    timeout = 5
    start = int(time.time())
    balance_sender, balance_receiver = (
        pygate_client.wallet.balance(wallets[0]),
        pygate_client.wallet.balance(wallets[1]),
    )
    while (
        balance_sender != 250000000000000000 or balance_receiver != 250000000000000000
    ):
        time.sleep(1)
        balance_sender, balance_receiver = (
            pygate_client.wallet.balance(wallets[0]),
            pygate_client.wallet.balance(wallets[1]),
        )
        now = int(time.time())
        if now - start > timeout:
            raise Exception("Waiting for wallets ot initialize timed out")

    amount = 100
    pygate_client.admin.wallet.send(sender, receiver, amount)

    time.sleep(3)

    assert balance_receiver + amount == pygate_client.wallet.balance(receiver)
