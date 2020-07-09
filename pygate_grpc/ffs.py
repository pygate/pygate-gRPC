import grpc

import proto.ffs_rpc_pb2 as ffs_rpc_pb2
import proto.ffs_rpc_pb2_grpc as ffs_rpc_pb2_grpc

TOKEN_KEY = 'x-ffs-token'

class FfsClient(object):
    def __init__(self, hostName):
        self.hostName = hostName
        channel = grpc.insecure_channel(hostName)
        self.client = ffs_rpc_pb2_grpc.RPCServiceStub(channel)

    def _getMetaData(self, token):
        return ((TOKEN_KEY, token),)

    def create(self):
        req = ffs_rpc_pb2.CreateRequest()
        return self.client.Create(req)

    def listApi(self):
        req = ffs_rpc_pb2.ListAPIRequest()
        return self.client.ListAPI(req)


    # The metadata is set in here https://github.com/textileio/js-powergate-client/blob/9d1ad04a7e1f2a6e18cc5627751f9cbddaf6fe05/src/util/grpc-helpers.ts#L7
    # Note that you can't have capital letter in meta data field, see here: https://stackoverflow.com/questions/45071567/how-to-send-custom-header-metadata-with-python-grpc
    def addrsList(self, token):
        req = ffs_rpc_pb2.AddrsRequest()
        return self.client.Addrs(req, metadata=self._getMetaData(token))

    def iD(self, token):
        req = ffs_rpc_pb2.IDRequest()
        return self.client.ID(req, metadata=self._getMetaData(token))

    def addToHot(self, chunks):
        # TODO: need to figure out how to send file chunk to server
        pass

    def logs(self, cid, token):
        req = ffs_rpc_pb2.WatchLogsRequest()
        req.setCid(cid)
        return self.client.WatchLogs(req, metadata=self._getMetaData(token))

    def info(self, cid, token):
        req = ffs_rpc_pb2.WatchLogsRequest(cid=cid)
        return self.client.Info(req, metadata=self._getMetaData(token))


