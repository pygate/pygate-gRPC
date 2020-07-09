import grpc
import logging
import proto.health_rpc_pb2 as health_rpc_pb2
import proto.health_rpc_pb2_grpc as health_rpc_pb2_grpc

logger = logging.getLogger(__name__)


class HealthClient(object):
    def __init__(self, host_name):
        channel = grpc.insecure_channel(host_name)
        self.client = health_rpc_pb2_grpc.RPCServiceStub(channel)

    def check(self):
        req = health_rpc_pb2.CheckRequest()
        return self.client.Check(req)
