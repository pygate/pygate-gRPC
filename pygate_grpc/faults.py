from proto import faults_rpc_pb2, faults_rpc_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta


class FaultsClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel):
        self.client = faults_rpc_pb2_grpc.RPCServiceStub(channel)

    def get(self):
        req = faults_rpc_pb2.GetRequest()
        return self.client.Get(req)
