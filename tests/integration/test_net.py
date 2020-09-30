import logging

from pygate_grpc.client import PowerGateClient
from proto.net_rpc_pb2 import (
    ListenAddrResponse,
    PeersResponse,
    FindPeerResponse,
    ConnectPeerResponse,
    DisconnectPeerResponse,
    ConnectPeerResponse,
)
import time

logger = logging.getLogger(__name__)


def test_grpc_net_listen_adderess(pygate_client: PowerGateClient):
    res = pygate_client.net.listen_adderess()

    assert res is not None
    assert type(res) == ListenAddrResponse
    assert res.addr_info is not None


def test_grpc_net_peers(pygate_client: PowerGateClient):
    res = pygate_client.net.peers()

    assert res is not None
    assert type(res) == PeersResponse
    # It should connect to at least 1 peer.
    assert len(res.peers) > 0


def test_grpc_net_find_peer(pygate_client: PowerGateClient):
    res = pygate_client.net.peers()

    assert res is not None
    assert type(res) == PeersResponse
    # It should connect to at least 1 peer.
    assert len(res.peers) > 0

    peer_id = res.peers[0].addr_info.id
    res = pygate_client.net.find_peer(peer_id)

    assert res is not None
    assert type(res) == FindPeerResponse
    assert res.peer_info.addr_info.id == peer_id


def test_grpc_net_connect_peer(pygate_client: PowerGateClient):
    pass


def test_grpc_net_disconnect_peer(pygate_client: PowerGateClient):
    pass


def test_grpc_net_connectedness(pygate_client: PowerGateClient):
    pass
