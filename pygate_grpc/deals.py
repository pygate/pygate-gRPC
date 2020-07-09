import grpc

import proto.deals_rpc_pb2 as deals_rpc_pb2
import proto.deals_rpc_pb2_grpc as deals_rpc_pb2_grpc


class DealsClient(object):
    ## THIS USED AN OUTDATED PROTO SPECIFICATION IT NEEDS RE DEVELOPMENT
    def __init__(self, host_name):
        channel = grpc.insecure_channel(host_name)
        self.client = deals_rpc_pb2_grpc.RPCServiceStub(channel)

    def final_deal_records(self):
        req = deals_rpc_pb2.FinalDealRecordsRequest()
        return self.client.FinalDealRecords(req)

    def pending_deal_records(self):
        req = deals_rpc_pb2.PendingDealRecordsRequest()
        return self.client.PendingDealRecords(req)
