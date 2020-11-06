from typing import List
from proto.powergate.v1 import powergate_pb2, powergate_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta


class DealsClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = powergate_pb2_grpc.PowergateServiceStub(channel)
        self.get_metadata = get_metadata

    def storage_deal_records(
        self,
        include_final=True,
        include_pending=False,
        from_addrs: List[str] = None,
        data_cids: List[str] = None,
        ascending: bool = False,
        token: str = None,
    ):
        deal_config = powergate_pb2.DealRecordsConfig(
            from_addrs=from_addrs,
            data_cids=data_cids,
            include_pending=include_pending,
            include_final=include_final,
            ascending=ascending,
        )
        req = powergate_pb2.StorageDealRecordsRequest(config=deal_config)
        return self.client.StorageDealRecords(req, metadata=self.get_metadata(token))

    def retrieval_deal_records(
        self,
        include_final=True,
        include_pending=False,
        from_addrs: List[str] = None,
        data_cids: List[str] = None,
        ascending: bool = False,
        token: str = None,
    ):
        deal_config = powergate_pb2.DealRecordsConfig(
            from_addrs=from_addrs,
            data_cids=data_cids,
            include_pending=include_pending,
            include_final=include_final,
            ascending=ascending,
        )
        req = powergate_pb2.RetrievalDealRecordsRequest(config=deal_config)
        return self.client.RetrievalDealRecords(req, metadata=self.get_metadata(token))
