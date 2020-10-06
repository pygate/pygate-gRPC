from typing import Iterable, List, Tuple

from deprecated import deprecated
from google.protobuf.json_format import Parse

from proto import ffs_rpc_pb2, ffs_rpc_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta, future_error_handler

TOKEN_KEY = "x-ffs-token"
CHUNK_SIZE = 1024 * 1024  # 1MB


def _generate_chunks(chunks: Iterable[bytes]) -> Iterable[ffs_rpc_pb2.StageRequest]:
    for chunk in chunks:
        yield ffs_rpc_pb2.StageRequest(chunk=chunk)


def chunks_to_bytes(chunks: Iterable[ffs_rpc_pb2.StageRequest]) -> Iterable[bytes]:
    for c in chunks:
        yield c.chunk


def bytes_to_chunks(bytes_iter: Iterable[bytes],) -> Iterable[ffs_rpc_pb2.StageRequest]:
    for b in bytes_iter:
        yield ffs_rpc_pb2.StageRequest(chunk=b)


def get_file_bytes(filename: str):
    with open(filename, "rb") as f:
        while True:
            piece = f.read(CHUNK_SIZE)
            if len(piece) == 0:
                return
            yield piece


class FfsClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel):
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
        return self.client.ID(req, metadata=self._get_meta_data(token))

    def addrs_list(self, token: str = None):
        req = ffs_rpc_pb2.AddrsRequest()
        return self.client.Addrs(req, metadata=self._get_meta_data(token))

    def addrs_new(
        self, name: str, type_: str = "", is_default: bool = False, token: str = None
    ):
        req = ffs_rpc_pb2.NewAddrRequest(
            name=name, address_type=type_, make_default=is_default
        )
        return self.client.NewAddr(req, metadata=self._get_meta_data(token))

    def sign_message(self, addr: str, msg: bytes, token: str = None):
        req = ffs_rpc_pb2.SignMessageRequest(addr=addr, msg=msg)
        return self.client.SignMessage(req, metadata=self._get_meta_data(token))

    def verify_message(
        self, addr: str, msg: bytes, signature: bytes, token: str = None
    ):
        req = ffs_rpc_pb2.VerifyMessageRequest(addr=addr, msg=msg, signature=signature)
        return self.client.VerifyMessage(req, metadata=self._get_meta_data(token))

    def default_config(self, token: str = None):
        req = ffs_rpc_pb2.DefaultStorageConfigRequest()
        return self.client.DefaultStorageConfig(
            req, metadata=self._get_meta_data(token)
        )

    def default_config_for_cid(self, cid: str, token: str = None):
        req = ffs_rpc_pb2.GetStorageConfigRequest(cid=cid)
        return self.client.GetStorageConfig(req, metadata=self._get_meta_data(token))

    # Currently you need to pass in the ffs_rpc_pb2.DefaultConfig. However, this is not a good design.
    def set_default_config(self, config: str, token: str = None):
        config = Parse(config, ffs_rpc_pb2.StorageConfig())
        req = ffs_rpc_pb2.SetDefaultStorageConfigRequest(config=config)
        return self.client.SetDefaultStorageConfig(
            req, metadata=self._get_meta_data(token)
        )

    def show(self, cid: str, token: str = None):
        req = ffs_rpc_pb2.ShowRequest(cid=cid)
        return self.client.Show(req, metadata=self._get_meta_data(token))

    # Note that the chunkIter should be an iterator that yield `ffs_rpc_pb2.AddToHotRequest`,
    # it is the caller's responsibility to create the iterator.
    # The provided getFileChunks comes in handy some times.
    # TODO: deprecate this.
    @deprecated(version="0.0.6", reason="This method is deprecated")
    def add_to_hot(
        self, chunks_iter: Iterable[ffs_rpc_pb2.StageRequest], token: str = None
    ):
        return self.client.Stage(chunks_iter, metadata=self._get_meta_data(token))

    def stage(self, chunks_iter: Iterable[ffs_rpc_pb2.StageRequest], token: str = None):
        return self.client.Stage(chunks_iter, metadata=self._get_meta_data(token))

    # This will return an iterator which callers can look through
    def get(self, cid: str, token: str = None) -> Iterable[bytes]:
        req = ffs_rpc_pb2.GetRequest(cid=cid)
        chunks = self.client.Get(req, metadata=self._get_meta_data(token))
        return chunks_to_bytes(chunks)

    def send_fil(self, sender: str, receiver: str, amount: int, token: str = None):
        # To avoid name collision since `from` is reserved in Python.
        kwargs = {"from": sender, "to": receiver, "amount": amount}
        req = ffs_rpc_pb2.SendFilRequest(**kwargs)
        return self.client.SendFil(req, metadata=self._get_meta_data(token))

    @future_error_handler
    def logs(self, cid, token: str = None, history: bool = False, timeout: int = None):
        req = ffs_rpc_pb2.WatchLogsRequest(cid=cid, history=history)
        return self.client.WatchLogs(
            req, metadata=self._get_meta_data(token), timeout=timeout
        )

    def info(self, cid, token: str = None):
        req = ffs_rpc_pb2.WatchLogsRequest(cid=cid)
        return self.client.Info(req, metadata=self._get_meta_data(token))

    def get_storage_job(self, jid: str, token: str = None):
        req = ffs_rpc_pb2.GetStorageJobRequest(jid=jid)
        return self.client.GetStorageJob(req, metadata=self._get_meta_data(token))

    def push(
        self, cid, token: str = None,
    ):
        req = ffs_rpc_pb2.PushStorageConfigRequest(cid=cid)
        return self.client.PushStorageConfig(req, metadata=self._get_meta_data(token))

    def close(self, token: str = None):
        req = ffs_rpc_pb2.CloseRequest()
        return self.client.Close(req, metadata=self._get_meta_data(token))

    def list_pay_channel(self, token: str = None):
        req = ffs_rpc_pb2.ListPayChannelsRequest()
        return self.client.ListPayChannels(req, metadata=self._get_meta_data(token))

    def create_pay_channel(
        self, sender: str, receiver: str, amount: int, token: str = None
    ):
        kwargs = {"from": sender, "to": receiver, "amount": amount}
        req = ffs_rpc_pb2.CreateRequest(kwargs)
        return self.client.CreatePayChannel(req, metadata=self._get_meta_data(token))

    def redeem_pay_channel(
        self, sender: str, receiver: str, amount: int, token: str = None
    ):
        kwargs = {"from": sender, "to": receiver, "amount": amount}
        req = ffs_rpc_pb2.CreateRequest(kwargs)
        return self.client.CreatePayChannel(req, metadata=self._get_meta_data(token))

    def list_storage_deal_records(
        self,
        include_final=True,
        include_pending=False,
        from_addrs: List[str] = None,
        data_cids: List[str] = None,
        ascending: bool = False,
        token: str = None,
    ):
        deal_config = ffs_rpc_pb2.ListDealRecordsConfig(
            from_addrs=from_addrs,
            data_cids=data_cids,
            include_pending=include_pending,
            include_final=include_final,
            ascending=ascending,
        )
        req = ffs_rpc_pb2.ListStorageDealRecordsRequest(config=deal_config)
        return self.client.ListStorageDealRecords(
            req, metadata=self._get_meta_data(token)
        )

    def list_retrieval_deal_records(
        self,
        include_final=True,
        include_pending=False,
        from_addrs: List[str] = None,
        data_cids: List[str] = None,
        ascending: bool = False,
        token: str = None,
    ):
        deal_config = ffs_rpc_pb2.ListDealRecordsConfig(
            from_addrs=from_addrs,
            data_cids=data_cids,
            include_pending=include_pending,
            include_final=include_final,
            ascending=ascending,
        )
        req = ffs_rpc_pb2.ListRetrievalDealRecordsRequest(config=deal_config)
        return self.client.ListRetrievalDealRecords(
            req, metadata=self._get_meta_data(token)
        )

    # The metadata is set in here https://github.com/textileio/js-powergate-client/blob
    # /9d1ad04a7e1f2a6e18cc5627751f9cbddaf6fe05/src/util/grpc-helpers.ts#L7 Note that you can't have capital letter in
    # meta data field, see here: https://stackoverflow.com/questions/45071567/how-to-send-custom-header-metadata-with
    # -python-grpc
    def _get_meta_data(self, token: str) -> Tuple[Tuple[str, str]]:
        if token is not None:
            return ((TOKEN_KEY, token),)
        if self.token is not None:
            return ((TOKEN_KEY, self.token),)
        self._raise_no_token_provided_exception()

    def _raise_no_token_provided_exception(self):
        raise Exception(
            "No token is provided, you should either call the set_token method to set"
            + " the token, or supplied the token in the method."
        )
