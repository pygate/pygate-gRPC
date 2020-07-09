import logging

from proto.ffs_rpc_pb2 import CreateResponse
from pygate_grpc.client import PowerGateClient

logger = logging.getLogger(__name__)


def test_grpc_ffs_create(pygate_client: PowerGateClient):
    ## Raises an error for some reason
    res = pygate_client.ffs.create()

    assert type(res) == CreateResponse
    assert res.id is not None
    assert res.token is not None

