import logging
import pytest

from proto.ffs_rpc_pb2 import CreateResponse, AddToHotRequest
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
    res = pygate_client.ffs.list_api()

    assert res is not None
    assert ffs_instance.id in res.instances


def test_grpc_ffs_add_to_hot(pygate_client: PowerGateClient, ffs_instance):
    res = pygate_client.ffs.add_to_hot(test_chunks(), ffs_instance.token)

    assert res is not None
    assert res.cid is not None

def test_chunks():
    for _ in range(1):
        yield AddToHotRequest(chunk=bytes("test_content", "ASCII"))
