import logging

from proto.faults_rpc_pb2 import GetResponse, Index
from pygate_grpc.client import PowerGateClient

logger = logging.getLogger(__name__)


def test_grpc_faults(pygate_client: PowerGateClient):
    res = pygate_client.faults.get()

    assert type(res) == GetResponse
    assert type(res.index) == Index
    assert res.index.tipsetkey is not None
