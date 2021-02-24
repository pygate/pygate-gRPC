from typing import List

from powergate.user.v1 import user_pb2, user_pb2_grpc

from pygate_grpc.decorators import unmarshal_with
from pygate_grpc.errors import ErrorHandlerMeta
from pygate_grpc.types import StorageInfo


class StorageInfoClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = user_pb2_grpc.UserServiceStub(channel)
        self.get_metadata = get_metadata

    @unmarshal_with(StorageInfo)
    def get(self, cid: str, token: str = None) -> StorageInfo:
        req = user_pb2.StorageInfoRequest(cid=cid)
        return self.client.StorageInfo(
            req, metadata=self.get_metadata(token)
        ).storage_info

    @unmarshal_with(StorageInfo, many=True)
    def list(self, cids: List[str], token: str = None) -> List[StorageInfo]:
        req = user_pb2.ListStorageInfoRequest(cids=cids)
        return self.client.ListStorageInfo(
            req, metadata=self.get_metadata(token)
        ).storage_info
