import grpc

from proto import faults_rpc_pb2
from proto import faults_rpc_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta


class FaultsClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, host_name, is_secure):
        channel = (
            grpc.secure_channel(host_name, grpc.ssl_channel_credentials())
            if is_secure
            else grpc.insecure_channel(host_name)
        )
        self.client = faults_rpc_pb2_grpc.RPCServiceStub(channel)

    def get(self):
        req = faults_rpc_pb2.GetRequest()
        return self.client.Get(req)
