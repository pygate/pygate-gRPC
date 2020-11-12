from typing import List, Iterable
from powergate.user.v1 import user_pb2, user_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta, future_error_handler

CHUNK_SIZE = 1024 * 1024  # 1MB


def _generate_chunks(chunks: Iterable[bytes]) -> Iterable[user_pb2.StageRequest]:
    for chunk in chunks:
        yield user_pb2.StageRequest(chunk=chunk)


def chunks_to_bytes(chunks: Iterable[user_pb2.StageRequest]) -> Iterable[bytes]:
    for c in chunks:
        yield c.chunk


def bytes_to_chunks(bytes_iter: Iterable[bytes],) -> Iterable[user_pb2.StageRequest]:
    for b in bytes_iter:
        yield user_pb2.StageRequest(chunk=b)


def get_file_bytes(filename: str):
    with open(filename, "rb") as f:
        while True:
            piece = f.read(CHUNK_SIZE)
            if len(piece) == 0:
                return
            yield piece


class DataClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = user_pb2_grpc.UserServiceStub(channel)
        self.get_metadata = get_metadata

    def stage(self, chunks_iter: Iterable[user_pb2.StageRequest], token: str = None):
        return self.client.Stage(chunks_iter, metadata=self.get_metadata(token))

    def replace_data(self, cid1: str, cid2: str, token: str = None):
        req = user_pb2.ReplaceDataRequest(cid1=cid1, cid2=cid2)
        return self.client.ReplaceData(req, metadata=self.get_metadata(token))

    # This will return an iterator which callers can look through
    def get(self, cid: str, token: str = None) -> Iterable[bytes]:
        req = user_pb2.GetRequest(cid=cid)
        chunks = self.client.Get(req, metadata=self.get_metadata(token))
        return chunks_to_bytes(chunks)

    @future_error_handler
    def watch_logs(
        self, cid, token: str = None, history: bool = False, timeout: int = None
    ):
        req = user_pb2.WatchLogsRequest(cid=cid, history=history)
        return self.client.WatchLogs(
            req, metadata=self.get_metadata(token), timeout=timeout
        )

    def cid_info(self, cids: List[str], token: str = None):
        req = user_pb2.CidInfoRequest(cids=cids)
        return self.client.CidInfo(req, metadata=self.get_metadata(token))
