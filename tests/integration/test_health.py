import logging

from pygate_grpc.client import PowerGateClient
from proto.health_rpc_pb2 import CheckResponse, STATUS_OK

logger = logging.getLogger(__name__)


def test_grpc_health(pygate_client: PowerGateClient):
    res = pygate_client.health.check()

    assert type(res) == CheckResponse
    assert res.status == STATUS_OK
    assert res.messages == []
