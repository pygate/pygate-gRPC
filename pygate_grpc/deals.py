from typing import List

from powergate.user.v1 import user_pb2, user_pb2_grpc

from pygate_grpc.decorators import unmarshal_with
from pygate_grpc.errors import ErrorHandlerMeta


class DealsClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = user_pb2_grpc.UserServiceStub(channel)
        self.get_metadata = get_metadata

    @unmarshal_with(many=True)
    def storage_deal_records(
        self,
        include_final=True,
        include_pending=False,
        from_addrs: List[str] = None,
        data_cids: List[str] = None,
        ascending: bool = False,
        token: str = None,
    ):
        deal_config = user_pb2.DealRecordsConfig(
            from_addrs=from_addrs,
            data_cids=data_cids,
            include_pending=include_pending,
            include_final=include_final,
            ascending=ascending,
        )
        req = user_pb2.StorageDealRecordsRequest(config=deal_config)
        return self.client.StorageDealRecords(
            req, metadata=self.get_metadata(token)
        ).records

    @unmarshal_with(many=True)
    def retrieval_deal_records(
        self,
        include_final=True,
        include_pending=False,
        from_addrs: List[str] = None,
        data_cids: List[str] = None,
        ascending: bool = False,
        token: str = None,
    ):
        deal_config = user_pb2.DealRecordsConfig(
            from_addrs=from_addrs,
            data_cids=data_cids,
            include_pending=include_pending,
            include_final=include_final,
            ascending=ascending,
        )
        req = user_pb2.RetrievalDealRecordsRequest(config=deal_config)
        return self.client.RetrievalDealRecords(
            req, metadata=self.get_metadata(token)
        ).records
