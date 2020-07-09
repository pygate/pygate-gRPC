import logging
import pytest

from proto.ffs_rpc_pb2 import CreateResponse
from pygate_grpc.client import PowerGateClient

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def ffs_instance(pygate_client: PowerGateClient):
    return pygate_client.ffs.create()


def test_grpc_ffs_create(pygate_client: PowerGateClient):
    ## Raises an error for some reason
    res = pygate_client.ffs.create()

    assert type(res) == CreateResponse
    assert res.id is not None
    assert res.token is not None


def test_grpc_ffs_list_api(pygate_client: PowerGateClient, ffs_instance):
    res = pygate_client.ffs.list_api()
    print(res)
