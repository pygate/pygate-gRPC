from itertools import islice
from typing import Iterable, List

from deprecated import deprecated
from powergate.user.v1 import user_pb2, user_pb2_grpc

from pygate_grpc.decorators import unmarshal_with
from pygate_grpc.errors import ErrorHandlerMeta, future_error_handler
from pygate_grpc.types import CidInfo, StagedFile

CHUNK_SIZE = 1024 * 1024  # 1MB


def _generate_chunks(chunks: Iterable[bytes]) -> Iterable[user_pb2.StageRequest]:
    for chunk in chunks:
        yield user_pb2.StageRequest(chunk=chunk)


def chunks_to_bytes(chunks: Iterable[user_pb2.StageRequest]) -> Iterable[bytes]:
    for c in chunks:
        yield c.chunk


@deprecated(version="1.0.0", reason="You should use byte_chunks_iter function instead")
def bytes_to_chunks(bytes_iter: Iterable[bytes],) -> Iterable[user_pb2.StageRequest]:
    for b in bytes_iter:
        yield user_pb2.StageRequest(chunk=b)


@deprecated(
    version="1.0.0", reason="You should use byte_chunks_iter_from_file function instead"
)
def get_file_bytes(filename: str):
    with open(filename, "rb") as f:
        while True:
            piece = f.read(CHUNK_SIZE)
            if len(piece) == 0:
                return
            yield piece


def byte_chunks_iter(bts: bytes, chunk_size: int = CHUNK_SIZE):
    it = iter(bts)
    while True:
        chunk = bytes(islice(it, chunk_size))
        if not chunk:
            break
        yield user_pb2.StageRequest(chunk=chunk)


def byte_chunks_iter_from_file(filepath: str, chunk_size: int = CHUNK_SIZE):
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                return
            yield user_pb2.StageRequest(chunk=chunk)


class DataClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = user_pb2_grpc.UserServiceStub(channel)
        self.get_metadata = get_metadata

    @deprecated(
        version="1.0.0",
        reason="You should use `stage_file` or `stage_bytes` function instead",
    )
    def stage(self, chunks_iter: Iterable[user_pb2.StageRequest], token: str = None):
        return self.client.Stage(chunks_iter, metadata=self.get_metadata(token))

    @unmarshal_with(StagedFile)
    def stage_bytes(
        self, bts: bytes, token: str = None, chunk_size: int = CHUNK_SIZE
    ) -> StagedFile:
        chunks_iter = byte_chunks_iter(bts, chunk_size=chunk_size)
        return self.client.Stage(chunks_iter, metadata=self.get_metadata(token))

    @unmarshal_with(StagedFile)
    def stage_file(
        self, filepath: str, token: str = None, chunk_size: int = CHUNK_SIZE
    ) -> StagedFile:
        chunks_iter = byte_chunks_iter_from_file(filepath, chunk_size=chunk_size)
        return self.client.Stage(chunks_iter, metadata=self.get_metadata(token))

    def replace_data(self, cid1: str, cid2: str, token: str = None):
        req = user_pb2.ReplaceDataRequest(cid1=cid1, cid2=cid2)
        return self.client.ReplaceData(req, metadata=self.get_metadata(token))

    def get(self, cid: str, token: str = None) -> bytes:
        req = user_pb2.GetRequest(cid=cid)
        chunks = self.client.Get(req, metadata=self.get_metadata(token))
        return b"".join(map(lambda c: c.chunk, chunks))

    @future_error_handler
    def watch_logs(
        self, cid, token: str = None, history: bool = False, timeout: int = None
    ):
        req = user_pb2.WatchLogsRequest(cid=cid, history=history)
        return self.client.WatchLogs(
            req, metadata=self.get_metadata(token), timeout=timeout
        )

    @unmarshal_with(CidInfo, many=True)
    def cid_info(self, cids: List[str], token: str = None) -> List[CidInfo]:
        req = user_pb2.CidInfoRequest(cids=cids)
        return self.client.CidInfo(req, metadata=self.get_metadata(token)).cid_infos
