import grpc

from proto import buildinfo_rpc_pb2
from proto import buildinfo_rpc_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta


class BuildinfoClient(object, metaclass=ErrorHandlerMeta):
    ## THIS USED AN OUTDATED PROTO SPECIFICATION IT NEEDS RE DEVELOPMENT
    def __init__(self, host_name, is_secure):
        channel = (
            grpc.secure_channel(host_name, grpc.ssl_channel_credentials())
            if is_secure
            else grpc.insecure_channel(host_name)
        )
        self.client = buildinfo_rpc_pb2_grpc.RPCServiceStub(channel)

    def final_records(self):
        req = buildinfo_rpc_pb2.BuildInfoRequest()
        return self.client.BuildInfo(req)
