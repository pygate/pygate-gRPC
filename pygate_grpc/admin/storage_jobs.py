from typing import List

from powergate.admin.v1 import admin_pb2, admin_pb2_grpc

from pygate_grpc.errors import ErrorHandlerMeta


class StorageJobsClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = admin_pb2_grpc.AdminServiceStub(channel)
        self.get_metadata = get_metadata

    def queued(self, user_id: str, cids: List[str], admin_token: str = None):
        req = admin_pb2.QueuedStorageJobsRequest(cids=cids, user_id=user_id)
        return self.client.QueuedStorageJobs(
            req, metadata=self.get_metadata(admin_token)
        )

    def executing(self, user_id: str, cids: List[str], admin_token: str = None):
        req = admin_pb2.ExecutingStorageJobsRequest(cids=cids, user_id=user_id)
        return self.client.ExecutingStorageJobs(
            req, metadata=self.get_metadata(admin_token)
        )

    def latest_final(self, user_id: str, cids: List[str], admin_token: str = None):
        req = admin_pb2.LatestFinalStorageJobsRequest(cids=cids, user_id=user_id)
        return self.client.LatestFinalStorageJobs(
            req, metadata=self.get_metadata(admin_token)
        )

    def latest_successful(self, user_id: str, cids: List[str], admin_token: str = None):
        req = admin_pb2.LatestSuccessfulStorageJobsRequest(cids=cids, user_id=user_id)
        return self.client.LatestSuccessfulStorageJobs(
            req, metadata=self.get_metadata(admin_token)
        )

    def summary(self, user_id: str, cids: List[str], admin_token: str = None):
        req = admin_pb2.StorageJobsSummaryRequest(cids=cids, user_id=user_id)
        return self.client.StorageJobsSummary(
            req, metadata=self.get_metadata(admin_token)
        )
