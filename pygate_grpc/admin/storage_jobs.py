from typing import List
from proto.admin.v1 import powergate_admin_pb2, powergate_admin_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta


class StorageJobsClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = powergate_admin_pb2_grpc.PowergateAdminServiceStub(channel)
        self.get_metadata = get_metadata

    def queued(self, profile_id: str, cids: List[str], admin_token: str = None):
        req = powergate_admin_pb2.QueuedStorageJobsRequest(
            cids=cids, profile_id=profile_id
        )
        return self.client.QueuedStorageJobs(
            req, metadata=self.get_metadata(admin_token)
        )

    def executing(self, profile_id: str, cids: List[str], admin_token: str = None):
        req = powergate_admin_pb2.ExecutingStorageJobsRequest(
            cids=cids, profile_id=profile_id
        )
        return self.client.ExecutingStorageJobs(
            req, metadata=self.get_metadata(admin_token)
        )

    def latest_final(self, profile_id: str, cids: List[str], admin_token: str = None):
        req = powergate_admin_pb2.LatestFinalStorageJobsRequest(
            cids=cids, profile_id=profile_id
        )
        return self.client.LatestFinalStorageJobs(
            req, metadata=self.get_metadata(admin_token)
        )

    def latest_successful(
        self, profile_id: str, cids: List[str], admin_token: str = None
    ):
        req = powergate_admin_pb2.LatestSuccessfulStorageJobsRequest(
            cids=cids, profile_id=profile_id
        )
        return self.client.LatestSuccessfulStorageJobs(
            req, metadata=self.get_metadata(admin_token)
        )

    def summary(self, profile_id: str, cids: List[str], admin_token: str = None):
        req = powergate_admin_pb2.StorageJobsSummaryRequest(
            cids=cids, profile_id=profile_id
        )
        return self.client.StorageJobsSummary(
            req, metadata=self.get_metadata(admin_token)
        )
