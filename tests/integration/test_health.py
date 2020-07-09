import logging

from pygate_grpc.health import HealthClient
from proto.health_rpc_pb2 import CheckResponse, STATUS_OK

logger = logging.getLogger(__name__)


def test_grpc_health(pygate_health_client: HealthClient):
    ## Raises an error for some reason
    res = pygate_health_client.check()
