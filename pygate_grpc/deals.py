import grpc

import proto.deals_rpc_pb2 as deals_rpc_pb2 
import proto.deals_rpc_pb2_grpc as deals_rpc_pb2_grpc

class DealsClient(object):
    def __init__(self, hostName):
        channel = grpc.insecure_channel(hostName)
        self.client = deals_rpc_pb2_grpc.RPCServiceStub(channel)

    def finalDealRecords(self):
        req = deals_rpc_pb2.FinalDealRecordsRequest()
        return self.client.FinalDealRecords(req)

    def pendingDealRecordsRequest(self):
        req = deals_rpc_pb2.PendingDealRecordsRequest()
        return self.client.PendingDealRecords(req)


if __name__ == "__main__":
    c = DealsClient("127.0.0.1:5002")
    print(c.finalDealRecords())
    print(c.pendingDealRecordsRequest())