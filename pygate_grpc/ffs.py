import grpc

from typing import Iterable, Tuple
from proto import ffs_rpc_pb2
from proto import ffs_rpc_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta

TOKEN_KEY = "x-ffs-token"
CHUNK_SIZE = 1024 * 1024  # 1MB


# The metadata is set in here https://github.com/textileio/js-powergate-client/blob
# /9d1ad04a7e1f2a6e18cc5627751f9cbddaf6fe05/src/util/grpc-helpers.ts#L7 Note that you can't have capital letter in
# meta data field, see here: https://stackoverflow.com/questions/45071567/how-to-send-custom-header-metadata-with
# -python-grpc
def _get_meta_data(token: str) -> Tuple[Tuple[str, str]]:
    return ((TOKEN_KEY, token),)


def _generate_chunks(chunks: Iterable[bytes]) -> Iterable[ffs_rpc_pb2.AddToHotRequest]:
    for chunk in chunks:
        yield ffs_rpc_pb2.AddToHotRequest(chunk=chunk)


def chunks_to_bytes(chunks: Iterable[ffs_rpc_pb2.AddToHotResponse]) -> Iterable[bytes]:
    for c in chunks:
        yield c.chunk


def bytes_to_chunks(
    bytes_iter: Iterable[bytes],
) -> Iterable[ffs_rpc_pb2.AddToHotRequest]:
    for b in bytes_iter:
        yield ffs_rpc_pb2.AddToHotRequest(chunk=b)


def get_file_bytes(filename: str):
    with open(filename, "rb") as f:
        while True:
            piece = f.read(CHUNK_SIZE)
            if len(piece) == 0:
                return
            yield piece


class FfsClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, host_name: str):
        self.host_name = host_name
        channel = grpc.insecure_channel(host_name)
        self.client = ffs_rpc_pb2_grpc.RPCServiceStub(channel)
        self.token = None

    def set_token(self, token: str):
        self.token = token

    def create(self):
        req = ffs_rpc_pb2.CreateRequest()
        return self.client.Create(req)

    def list_ffs(self):
        req = ffs_rpc_pb2.ListAPIRequest()
        return self.client.ListAPI(req)

    def id(self, token: str):
        req = ffs_rpc_pb2.IDRequest()
        return self.client.ID(req, metadata=_get_meta_data(token))

    def addrs_list(self, token: str = None):
        req = ffs_rpc_pb2.AddrsRequest()
        if token is not None:
            return self.client.Addrs(req, metadata=_get_meta_data(token))
        if self.token is not None:
            return self.client.Addrs(req, metadata=_get_meta_data(self.token))
        self._raise_no_token_provided_exception()

    def addrs_new(
        self, name: str, type_: str = "", is_default: bool = False, token: str = None
    ):
        req = ffs_rpc_pb2.NewAddrRequest(
            name=name, address_type=type_, make_default=is_default
        )
        if token is not None:
            return self.client.NewAddr(req, metadata=_get_meta_data(token))
        if self.token is not None:
            return self.client.NewAddr(req, metadata=_get_meta_data(self.token))
        self._raise_no_token_provided_exception()

    def default_config(self, token: str = None):
        req = ffs_rpc_pb2.DefaultConfig()
        if token is not None:
            return self.client.DefaultConfig(req, metadata=_get_meta_data(token))
        if self.token is not None:
            return self.client.DefaultConfig(req, metadata=_get_meta_data(self.token))
        self._raise_no_token_provided_exception()

    def default_config_for_cid(self, cid: str, token: str = None):
        req = ffs_rpc_pb2.GetDefaultCidConfigRequest(cid=cid)
        if token is not None:
            return self.client.GetDefaultCidConfig(req, metadata=_get_meta_data(token))
        if self.token is not None:
            return self.client.GetDefaultCidConfig(
                req, metadata=_get_meta_data(self.token)
            )
        self._raise_no_token_provided_exception()

    # Currently you need to pass in the ffs_rpc_pb2.DefaultConfig. However, this is not a good design.
    def set_default_config(self, config: ffs_rpc_pb2.DefaultConfig, token: str = None):
        req = ffs_rpc_pb2.DefaultConfig(config=config)
        if token is not None:
            return self.client.SetDefaultConfig(req, metadata=_get_meta_data(token))
        if self.token is not None:
            return self.client.SetDefaultConfig(
                req, metadata=_get_meta_data(self.token)
            )
        self._raise_no_token_provided_exception()

    def show(self, cid: str, token: str = None):
        req = ffs_rpc_pb2.ShowRequest(cid=cid)
        if token is not None:
            return self.client.Show(req, metadata=_get_meta_data(token))
        if self.token is not None:
            return self.client.Show(req, metadata=_get_meta_data(self.token))
        self._raise_no_token_provided_exception()

    # Note that the chunkIter should be an iterator that yield `ffs_rpc_pb2.AddToHotRequest`,
    # it is the caller's responsibility to create the iterator.
    # The provided getFileChunks comes in handy some times.
    def add_to_hot(
        self, chunks_iter: Iterable[ffs_rpc_pb2.AddToHotResponse], token: str = None
    ):
        return self.client.AddToHot(chunks_iter, metadata=_get_meta_data(token))

    # This will return an iterator which callers can look through
    def get(self, cid: str, token: str = None) -> Iterable[bytes]:
        req = ffs_rpc_pb2.GetRequest(cid=cid)
        chunks = self.client.Get(req, metadata=_get_meta_data(token))
        return chunks_to_bytes(chunks)

    def send_fil(self, sender: str, receiver: str, amount: int, token: str = None):
        # To avoid name collision since `from` is reserved in Python.
        kwargs = {"from": sender, "to": receiver, "amount": amount}
        req = ffs_rpc_pb2.SendFilRequest(**kwargs)
        if token is not None:
            return self.client.SendFil(req, metadata=_get_meta_data(token))
        if self.token is not None:
            return self.client.SendFil(req, metadata=_get_meta_data(self.token))
        self._raise_no_token_provided_exception()

    def logs(self, cid, token: str = None):
        req = ffs_rpc_pb2.WatchLogsRequest(cid=cid)
        return self.client.WatchLogs(req, metadata=_get_meta_data(token))

    def info(self, cid, token: str = None):
        req = ffs_rpc_pb2.WatchLogsRequest(cid=cid)
        return self.client.Info(req, metadata=_get_meta_data(token))

    def push(self, cid, token: str = None):
        req = ffs_rpc_pb2.PushConfigRequest(cid=cid)
        return self.client.PushConfig(req, metadata=_get_meta_data(token))

    def _raise_no_token_provided_exception(self):
        raise Exception(
            "No token is provided, you should either call the set_token method to set"
            + " the token, or supplied the token in the method."
        )
