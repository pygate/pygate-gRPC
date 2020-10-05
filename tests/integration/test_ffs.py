import logging
from pygate_grpc.exceptions import GRPCTimeoutException
import pytest
import time

from proto.ffs_rpc_pb2 import CreateResponse, StageRequest, AddrInfo
from pygate_grpc.client import PowerGateClient

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def ffs_instance(pygate_client: PowerGateClient):
    return pygate_client.ffs.create()


def test_grpc_ffs_create(pygate_client: PowerGateClient):
    res = pygate_client.ffs.create()

    assert type(res) == CreateResponse
    assert res.id is not None
    assert res.token is not None


def test_grpc_ffs_list_api(pygate_client: PowerGateClient, ffs_instance):
    res = pygate_client.ffs.list_ffs()

    assert res is not None
    assert ffs_instance.id in res.instances


def test_grpc_ffs_add_to_hot(pygate_client: PowerGateClient, ffs_instance):
    res = pygate_client.ffs.add_to_hot(chunks(), ffs_instance.token)

    assert res is not None
    assert res.cid is not None


def test_grpc_ffs_add_then_get_content(pygate_client: PowerGateClient, ffs_instance):
    res = pygate_client.ffs.add_to_hot(chunks(), ffs_instance.token)

    assert res is not None

    pygate_client.ffs.push(res.cid, ffs_instance.token)
    f = pygate_client.ffs.get(res.cid, ffs_instance.token)

    assert next(f) == b"test_content"


def test_grpc_ffs_list_wallet(pygate_client: PowerGateClient, ffs_instance):
    res = pygate_client.ffs.addrs_list(token=ffs_instance.token)

    assert res is not None
    assert len(res.addrs) == 1
    assert res.addrs[0].name == "Initial Address"
    assert res.addrs[0].type == "bls"


def test_create_new_wallet_address(
    pygate_client: PowerGateClient, ffs_instance: CreateResponse
):
    new_addr_name = "test"
    addr = pygate_client.ffs.addrs_new(name=new_addr_name, token=ffs_instance.token)

    assert addr is not None
    assert addr.addr is not None

    res = pygate_client.ffs.addrs_list(token=ffs_instance.token)

    assert res is not None

    expected_addr = AddrInfo(name=new_addr_name, addr=addr.addr, type="bls")
    assert expected_addr in res.addrs


def test_send_fil(pygate_client: PowerGateClient, ffs_instance: CreateResponse):
    sender_addr_name = "fil_sender"
    sender_addr = pygate_client.ffs.addrs_new(
        name=sender_addr_name, token=ffs_instance.token
    )

    receiver_addr_name = "fil_receiver"
    receiver_addr = pygate_client.ffs.addrs_new(
        name=receiver_addr_name, token=ffs_instance.token
    )

    # Sleep a bit to wait for initialization
    time.sleep(5)
    before_sender_fil = pygate_client.wallet.balance(sender_addr.addr)
    before_receiver_fil = pygate_client.wallet.balance(receiver_addr.addr)

    pygate_client.ffs.send_fil(
        sender_addr.addr, receiver_addr.addr, 1, token=ffs_instance.token
    )

    # Wait a bit for transaction to complete
    time.sleep(5)
    after_sender_fil = pygate_client.wallet.balance(sender_addr.addr)
    after_receiver_fil = pygate_client.wallet.balance(receiver_addr.addr)

    assert before_sender_fil.balance > after_sender_fil.balance
    assert before_receiver_fil.balance < after_receiver_fil.balance


def test_ffs_logs(pygate_client: PowerGateClient, ffs_instance):
    ffs = pygate_client.ffs.create()

    stage_res = pygate_client.ffs.stage(chunks(), ffs.token)
    push_res = pygate_client.ffs.push(stage_res.cid, ffs.token)
    logs_res = pygate_client.ffs.logs(stage_res.cid, ffs.token, history=True, timeout=5)

    logs = []
    try:
        for f in logs_res:
            logs.append(f)
    except GRPCTimeoutException:
        pass

    assert len(logs) > 0


def chunks():
    for _ in range(1):
        yield StageRequest(chunk=bytes("test_content", "ASCII"))
