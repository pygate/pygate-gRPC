import logging
import grpc
import pytest

from pygate_grpc.health import HealthClient
from proto.health_rpc_pb2 import CheckResponse, STATUS_OK

logger = logging.getLogger(__name__)


def test_grpc_health(pygate_health_client: HealthClient):
    res = pygate_health_client.check()

    assert type(res) == CheckResponse
    assert res.status == STATUS_OK
    assert res.messages == []
