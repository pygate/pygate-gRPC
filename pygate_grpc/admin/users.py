from powergate.admin.v1 import admin_pb2, admin_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta


class UsersClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = admin_pb2_grpc.AdminServiceStub(channel)
        self.get_metadata = get_metadata

    def create(self, admin_token: str = None):
        req = admin_pb2.CreateUserRequest()
        return self.client.CreateUser(
            req, metadata=self.get_metadata(None, admin_token)
        )

    def list(self, admin_token: str = None):
        req = admin_pb2.UsersRequest()
        return self.client.Users(req, metadata=self.get_metadata(None, admin_token))
