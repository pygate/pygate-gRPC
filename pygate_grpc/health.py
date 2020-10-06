import logging

from proto import health_rpc_pb2, health_rpc_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta

logger = logging.getLogger(__name__)


class HealthClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel):
        self.client = health_rpc_pb2_grpc.RPCServiceStub(channel)

    def check(self):
        req = health_rpc_pb2.CheckRequest()
        return self.client.Check(req)
