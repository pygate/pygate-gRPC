import logging
import grpc
import pytest

from pygate_grpc.client import PowerGateClient
from proto.faults_rpc_pb2 import GetResponse, Index

logger = logging.getLogger(__name__)


def test_grpc_faults(pygate_client: PowerGateClient):
    res = pygate_client.faults.get()

    assert type(res) == GetResponse
    assert type(res.index) == Index
    assert res.index.tipsetkey is not None