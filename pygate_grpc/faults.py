import grpc

import proto.faults_rpc_pb2 as faults_rpc_pb2 
import proto.faults_rpc_pb2_grpc as faults_rpc_pb2_grpc

class FaultsClient(object):
    def __init__(self, hostName):
        channel = grpc.insecure_channel(hostName)
        self.client = faults_rpc_pb2_grpc.RPCServiceStub(channel)

    def get(self):
        req = faults_rpc_pb2.GetRequest()
        return self.client.Get(req)