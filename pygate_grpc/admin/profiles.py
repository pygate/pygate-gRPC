from proto.admin.v1 import powergate_admin_pb2, powergate_admin_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta


class ProfilesClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = powergate_admin_pb2_grpc.PowergateAdminServiceStub(channel)
        self.get_metadata = get_metadata

    def create_storage_profile(self, admin_token: str = None):
        req = powergate_admin_pb2.CreateStorageProfileRequest()
        return self.client.CreateStorageProfile(
            req, metadata=self.get_metadata(None, admin_token)
        )

    def storage_profiles(self, admin_token: str = None):
        req = powergate_admin_pb2.StorageProfilesRequest()
        return self.client.StorageProfiles(
            req, metadata=self.get_metadata(None, admin_token)
        )
