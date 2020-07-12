import grpc

import proto.ffs_rpc_pb2 as ffs_rpc_pb2
import proto.ffs_rpc_pb2_grpc as ffs_rpc_pb2_grpc

TOKEN_KEY = "x-ffs-token"
CHUNK_SIZE = 1024 * 1024  # 1MB


class FfsClient(object):
    def __init__(self, host_name):
        self.host_name = host_name
        channel = grpc.insecure_channel(host_name)
        self.client = ffs_rpc_pb2_grpc.RPCServiceStub(channel)

    def set_token(self, token):
        self.token = token

    def list_api(self):
        req = ffs_rpc_pb2.ListAPIRequest()
        return self.client.ListAPI(req)

    def id(self, token):
        req = ffs_rpc_pb2.IDRequest()
        return self.client.ID(req, metadata=self._get_meta_data(token))

    def addrs_list(self, token=None):
        req = ffs_rpc_pb2.AddrsRequest()
        if token != None:
            return self.client.Addrs(req, metadata=self._get_meta_data(token))
        if self.token != None:
            return self.client.Addrs(req, metadata=self._get_meta_data(self.token))
        self._raise_no_token_provided_exception()

    def addrs_new(self, name, type="", isDefault=False, token=None):
        req = ffs_rpc_pb2.NewAddrRequest(
            name=name, address_type=type, make_default=isDefault
        )
        if token != None:
            return self.client.NewAddr(req, metadata=self._get_meta_data(token))
        if self.token != None:
            return self.client.NewAddr(req, metadata=self._get_meta_data(self.token))
        self._raise_no_token_provided_exception()

    def default_config(self, token=None):
        req = ffs_rpc_pb2.DefaultConfig()
        if token != None:
            return self.client.DefaultConfig(req, metadata=self._get_meta_data(token))
        if self.token != None:
            return self.client.DefaultConfig(
                req, metadata=self._get_meta_data(self.token)
            )
        self._raise_no_token_provided_exception

    def create(self):
        req = ffs_rpc_pb2.CreateRequest()
        return self.client.Create(req)

    def default_config_for_cid(self, cid, token=None):
        req = ffs_rpc_pb2.GetDefaultCidConfigRequest(cid=cid)
        if token != None:
            return self.client.GetDefaultCidConfig(
                req, metadata=self._get_meta_data(token)
            )
        if self.token != None:
            return self.client.GetDefaultCidConfig(
                req, metadata=self._get_meta_data(self.token)
            )
        self._raise_no_token_provided_exception

    # Currently you need to pass in the ffs_rpc_pb2.DefaultConfig. However, this is not a good design.
    def set_default_config(self, config, token):
        req = ffs_rpc_pb2.DefaultConfig(config=config)
        if token != None:
            return self.client.SetDefaultConfig(
                req, metadata=self._get_meta_data(token)
            )
        if self.token != None:
            return self.client.SetDefaultConfig(
                req, metadata=self._get_meta_data(self.token)
            )
        self._raise_no_token_provided_exception

    def show(self, cid, token):
        req = ffs_rpc_pb2.ShowRequest(cid=cid)
        if token != None:
            return self.client.Show(req, metadata=self._get_meta_data(token))
        if self.token != None:
            return self.client.Show(req, metadata=self._get_meta_data(self.token))
        self._raise_no_token_provided_exception

    # Note that the chunkIter should be an iterator that yield `ffs_rpc_pb2.AddToHotRequest`,
    # it is the caller's responsibility to create the iterator.
    # The provided getFileChunks comes in handy some times.
    def add_to_hot(self, chunksIter, token):
        return self.client.AddToHot(chunksIter, metadata=self._get_meta_data(token))

    # This will return an iterator which callers can look through
    def get(self, cid, token):
        req = ffs_rpc_pb2.GetRequest(cid=cid)
        chunks = self.client.Get(req, metadata=self._get_meta_data(token))
        return self.chunks_to_bytes(chunks)

    def send_fil(self, sender, receiver, amount, token):
        req = ffs_rpc_pb2.SendFilRequest(sender, receiver, amount)
        if token != None:
            return self.client.SendFil(req, metadata=self._get_meta_data(token))
        if self.token != None:
            return self.client.SendFil(req, metadata=self._get_meta_data(self.token))
        self._raise_no_token_provided_exception

    def logs(self, cid, token):
        req = ffs_rpc_pb2.WatchLogsRequest(cid=cid)
        return self.client.WatchLogs(req, metadata=self._get_meta_data(token))

    def info(self, cid, token):
        req = ffs_rpc_pb2.WatchLogsRequest(cid=cid)
        return self.client.Info(req, metadata=self._get_meta_data(token))

    def push(self, cid, token):
        req = ffs_rpc_pb2.PushConfigRequest(cid=cid)
        return self.client.PushConfig(req, metadata=self._get_meta_data(token))

    def get_file_bytes(self, filename):
        with open(filename, "rb") as f:
            while True:
                piece = f.read(CHUNK_SIZE)
                if len(piece) == 0:
                    return
                yield piece

    def bytes_to_chunks(self, bytesIter):
        for b in bytesIter:
            yield ffs_rpc_pb2.AddToHotRequest(chunk=b)

    def chunks_to_bytes(self, chunks):
        for c in chunks:
            yield c.chunk

    # The metadata is set in here https://github.com/textileio/js-powergate-client/blob/9d1ad04a7e1f2a6e18cc5627751f9cbddaf6fe05/src/util/grpc-helpers.ts#L7
    # Note that you can't have capital letter in meta data field, see here: https://stackoverflow.com/questions/45071567/how-to-send-custom-header-metadata-with-python-grpc
    def _get_meta_data(self, token):
        return ((TOKEN_KEY, token),)

    def _generate_chunks(self, chunks):
        for chunk in chunks:
            yield ffs_rpc_pb2.AddToHotRequest(chunk=chunk)

    def _raise_no_token_provided_exception(self):
        raise Exception(
            "No token is provided, you should either call the set_token method to set"
            + " the token, or supplied the token in the method."
        )
