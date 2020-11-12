import logging
import time

import pytest

from powergate.user.v1.user_pb2 import AddrInfo, StageRequest
from powergate.admin.v1.admin_pb2 import (
    CreateUserResponse,
    User,
)
from pygate_grpc.client import PowerGateClient
from pygate_grpc.exceptions import GRPCTimeoutException

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def user(pygate_client: PowerGateClient):
    res = pygate_client.admin.users.create()
    return res.user


def test_grpc_user_create(pygate_client: PowerGateClient):
    res = pygate_client.admin.users.create()

    assert type(res) == CreateUserResponse
    assert res.user.id is not None
    assert res.user.token is not None


def test_grpc_user_list_api(pygate_client: PowerGateClient, user: User):
    res = pygate_client.admin.users.list()

    assert res is not None
    assert user in res.auth_entries


def test_grpc_stage(pygate_client: PowerGateClient, user: User):
    res = pygate_client.data.stage(chunks(), user.token)

    assert res is not None
    assert res.cid is not None


def test_grpc_stage_then_get_content(pygate_client: PowerGateClient, user: User):
    res = pygate_client.data.stage(chunks(), user.token)

    assert res is not None

    pygate_client.storage_config.apply(res.cid, token=user.token)
    f = pygate_client.data.get(res.cid, user.token)

    assert next(f) == b"test_content"


def test_grpc_list_wallet(pygate_client: PowerGateClient, user: User):
    res = pygate_client.wallet.addresses(token=user.token)

    assert res is not None
    assert len(res.addresses) == 1
    assert res.addresses[0].name == "Initial Address"
    assert res.addresses[0].type == "bls"


def test_create_new_wallet_address(pygate_client: PowerGateClient, user: User):
    new_addr_name = "test"
    new_addr_res = pygate_client.wallet.new_address(
        name=new_addr_name, token=user.token
    )

    assert new_addr_res is not None
    assert new_addr_res.address is not None

    res = pygate_client.wallet.addresses(token=user.token)

    assert res is not None

    expected_addr = AddrInfo(name=new_addr_name, addr=new_addr_res.addr, type="bls")
    assert expected_addr in res.addresses


def test_send_fil(pygate_client: PowerGateClient, user: User):
    sender_addr_name = "fil_sender"
    sender_addr = pygate_client.wallet.new_address(
        name=sender_addr_name, token=user.token
    )

    receiver_addr_name = "fil_receiver"
    receiver_addr = pygate_client.wallet.new_address(
        name=receiver_addr_name, token=user.token
    )

    # Sleep a bit to wait for initialization
    time.sleep(5)
    before_sender_fil = pygate_client.wallet.balance(sender_addr.addr)
    before_receiver_fil = pygate_client.wallet.balance(receiver_addr.addr)

    pygate_client.wallet.send_fil(
        sender_addr.addr, receiver_addr.addr, "1", token=user.token
    )

    # Wait a bit for transaction to complete
    time.sleep(5)
    after_sender_fil = pygate_client.wallet.balance(sender_addr.addr)
    after_receiver_fil = pygate_client.wallet.balance(receiver_addr.addr)

    assert before_sender_fil.balance > after_sender_fil.balance
    assert before_receiver_fil.balance < after_receiver_fil.balance


def test_logs(pygate_client: PowerGateClient):
    res = pygate_client.admin.users.create()

    stage_res = pygate_client.data.stage(chunks(), res.user.token)
    pygate_client.storage_config.apply(stage_res.cid, token=res.user.token)
    logs_res = pygate_client.data.watch_logs(
        stage_res.cid, res.user.token, history=True, timeout=5
    )

    logs = []
    try:
        for f in logs_res:
            logs.append(f)
    except GRPCTimeoutException:
        pass

    assert len(logs) > 0


def test_storage_deals(pygate_client: PowerGateClient):
    res = pygate_client.admin.users.create()

    stage_res = pygate_client.data.stage(chunks(), res.user.token)
    pygate_client.storage_config.apply(stage_res.cid, token=res.user.token)

    time.sleep(3)

    pygate_client.deals.storage_deal_records(
        include_pending=True, include_final=True, token=res.user.token
    )


def test_retrieval_deals(pygate_client: PowerGateClient):
    res = pygate_client.admin.users.create()

    stage_res = pygate_client.data.stage(chunks(), res.user.token)
    pygate_client.storage_config.apply(stage_res.cid, token=res.user.token)

    time.sleep(3)

    pygate_client.deals.retrieval_deal_records(
        include_pending=True, include_final=True, token=res.user.token
    )


def test_push_override(pygate_client: PowerGateClient):
    res = pygate_client.admin.users.create()

    stage_res = pygate_client.data.stage(chunks(), res.user.token)
    pygate_client.storage_config.apply(stage_res.cid, token=res.user.token)

    pygate_client.storage_config.apply(
        stage_res.cid, token=res.user.token, override=True
    )


def chunks():
    for _ in range(1):
        yield StageRequest(chunk=bytes("test_content", "ASCII"))
