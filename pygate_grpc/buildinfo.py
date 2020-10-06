from proto import buildinfo_rpc_pb2, buildinfo_rpc_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta


class BuildinfoClient(object, metaclass=ErrorHandlerMeta):
    # THIS USED AN OUTDATED PROTO SPECIFICATION IT NEEDS RE DEVELOPMENT
    def __init__(self, channel):
        self.client = buildinfo_rpc_pb2_grpc.RPCServiceStub(channel)

    def final_records(self):
        req = buildinfo_rpc_pb2.BuildInfoRequest()
        return self.client.BuildInfo(req)
