import logging
import time

import pytest

from proto.powergate.v1.powergate_pb2 import AddrInfo, StageRequest
from proto.admin.v1.powergate_admin_pb2 import CreateStorageProfileResponse, AuthEntry
from pygate_grpc.client import PowerGateClient
from pygate_grpc.exceptions import GRPCTimeoutException

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def auth_entry(pygate_client: PowerGateClient):
    res = pygate_client.admin.profiles.create_storage_profile()
    return res.auth_entry


def test_grpc_profile_create(pygate_client: PowerGateClient):
    res = pygate_client.admin.profiles.create_storage_profile()

    assert type(res) == CreateStorageProfileResponse
    assert res.auth_entry.id is not None
    assert res.auth_entry.token is not None


def test_grpc_profile_list_api(pygate_client: PowerGateClient, auth_entry: AuthEntry):
    res = pygate_client.admin.profiles.storage_profiles()

    assert res is not None
    assert auth_entry in res.auth_entries


def test_grpc_stage(pygate_client: PowerGateClient, auth_entry: AuthEntry):
    res = pygate_client.data.stage(chunks(), auth_entry.token)

    assert res is not None
    assert res.cid is not None


def test_grpc_stage_then_get_content(
    pygate_client: PowerGateClient, auth_entry: AuthEntry
):
    res = pygate_client.data.stage(chunks(), auth_entry.token)

    assert res is not None

    pygate_client.storage_config.apply(res.cid, token=auth_entry.token)
    f = pygate_client.data.get(res.cid, auth_entry.token)

    assert next(f) == b"test_content"


def test_grpc_list_wallet(pygate_client: PowerGateClient, auth_entry: AuthEntry):
    res = pygate_client.wallet.addresses(token=auth_entry.token)

    assert res is not None
    assert len(res.addresses) == 1
    assert res.addresses[0].name == "Initial Address"
    assert res.addresses[0].type == "bls"


def test_create_new_wallet_address(
    pygate_client: PowerGateClient, auth_entry: AuthEntry
):
    new_addr_name = "test"
    new_addr_res = pygate_client.wallet.new_address(
        name=new_addr_name, token=auth_entry.token
    )

    assert new_addr_res is not None
    assert new_addr_res.address is not None

    res = pygate_client.wallet.addresses(token=auth_entry.token)

    assert res is not None

    expected_addr = AddrInfo(name=new_addr_name, addr=new_addr_res.addr, type="bls")
    assert expected_addr in res.addresses


def test_send_fil(pygate_client: PowerGateClient, auth_entry: AuthEntry):
    sender_addr_name = "fil_sender"
    sender_addr = pygate_client.wallet.new_address(
        name=sender_addr_name, token=auth_entry.token
    )

    receiver_addr_name = "fil_receiver"
    receiver_addr = pygate_client.wallet.new_address(
        name=receiver_addr_name, token=auth_entry.token
    )

    # Sleep a bit to wait for initialization
    time.sleep(5)
    before_sender_fil = pygate_client.wallet.balance(sender_addr.addr)
    before_receiver_fil = pygate_client.wallet.balance(receiver_addr.addr)

    pygate_client.wallet.send_fil(
        sender_addr.addr, receiver_addr.addr, "1", token=auth_entry.token
    )

    # Wait a bit for transaction to complete
    time.sleep(5)
    after_sender_fil = pygate_client.wallet.balance(sender_addr.addr)
    after_receiver_fil = pygate_client.wallet.balance(receiver_addr.addr)

    assert before_sender_fil.balance > after_sender_fil.balance
    assert before_receiver_fil.balance < after_receiver_fil.balance


def test_logs(pygate_client: PowerGateClient):
    profile = pygate_client.admin.profiles.create_storage_profile()

    stage_res = pygate_client.data.stage(chunks(), profile.auth_entry.token)
    pygate_client.storage_config.apply(stage_res.cid, token=profile.auth_entry.token)
    logs_res = pygate_client.data.watch_logs(
        stage_res.cid, profile.auth_entry.token, history=True, timeout=5
    )

    logs = []
    try:
        for f in logs_res:
            logs.append(f)
    except GRPCTimeoutException:
        pass

    assert len(logs) > 0


def test_storage_deals(pygate_client: PowerGateClient):
    profile = pygate_client.admin.profiles.create_storage_profile()

    stage_res = pygate_client.data.stage(chunks(), profile.auth_entry.token)
    pygate_client.storage_config.apply(stage_res.cid, token=profile.auth_entry.token)

    time.sleep(3)

    pygate_client.deals.storage_deal_records(
        include_pending=True, include_final=True, token=profile.auth_entry.token
    )


def test_retrieval_deals(pygate_client: PowerGateClient):
    profile = pygate_client.admin.profiles.create_storage_profile()

    stage_res = pygate_client.data.stage(chunks(), profile.auth_entry.token)
    pygate_client.storage_config.apply(stage_res.cid, token=profile.auth_entry.token)

    time.sleep(3)

    pygate_client.deals.retrieval_deal_records(
        include_pending=True, include_final=True, token=profile.auth_entry.token
    )


def test_push_override(pygate_client: PowerGateClient):
    profile = pygate_client.admin.profiles.create_storage_profile()

    stage_res = pygate_client.data.stage(chunks(), profile.auth_entry.token)
    pygate_client.storage_config.apply(stage_res.cid, token=profile.auth_entry.token)

    pygate_client.storage_config.apply(
        stage_res.cid, token=profile.auth_entry.token, override=True
    )


def chunks():
    for _ in range(1):
        yield StageRequest(chunk=bytes("test_content", "ASCII"))
