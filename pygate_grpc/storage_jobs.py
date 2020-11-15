from typing import List

from powergate.user.v1 import user_pb2, user_pb2_grpc

from pygate_grpc.errors import ErrorHandlerMeta, future_error_handler


class StorageJobsClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = user_pb2_grpc.UserServiceStub(channel)
        self.get_metadata = get_metadata

    def storage_job(self, job_id: str, token: str = None):
        req = user_pb2.StorageJobRequest(job_id=job_id)
        return self.client.StorageJob(req, metadata=self.get_metadata(token))

    def storage_config_for_job(self, job_id: str, token: str = None):
        req = user_pb2.StorageConfigForJobRequest(job_id=job_id)
        return self.client.StorageConfigForJob(req, metadata=self.get_metadata(token))

    def queued(self, cids: List[str], token: str = None):
        req = user_pb2.QueuedStorageJobsRequest(cids=cids)
        return self.client.QueuedStorageJobs(req, metadata=self.get_metadata(token))

    def executing(self, cids: List[str], token: str = None):
        req = user_pb2.ExecutingStorageJobsRequest(cids=cids)
        return self.client.ExecutingStorageJobs(req, metadata=self.get_metadata(token))

    def latest_final(self, cids: List[str], token: str = None):
        req = user_pb2.LatestFinalStorageJobsRequest(cids=cids)
        return self.client.LatestFinalStorageJobs(
            req, metadata=self.get_metadata(token)
        )

    def latest_successful(self, cids: List[str], token: str = None):
        req = user_pb2.LatestSuccessfulStorageJobsRequest(cids=cids)
        return self.client.LatestSuccessfulStorageJobs(
            req, metadata=self.get_metadata(token)
        )

    def summary(self, cids: List[str], token: str = None):
        req = user_pb2.StorageJobsSummaryRequest(cids=cids)
        return self.client.StorageJobsSummary(req, metadata=self.get_metadata(token))

    @future_error_handler
    def watch(self, job_ids: List[str], token: str = None):
        req = user_pb2.WatchStorageJobsRequest(job_ids=job_ids)
        return self.client.WatchStorageJobs(req, metadata=self.get_metadata(token))

    def cancel(self, job_id: str, token: str = None):
        req = user_pb2.CancelStorageJobRequest(job_id=job_id)
        return self.client.CancelStorageJob(req, metadata=self.get_metadata(token))
