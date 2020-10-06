import logging

import proto.net_rpc_pb2 as net_rpc_pb2
import proto.net_rpc_pb2_grpc as net_rpc_pb2_grpc

logger = logging.getLogger(__name__)


class NetClient(object):
    def __init__(self, channel):
        self.client = net_rpc_pb2_grpc.RPCServiceStub(channel)

    def listen_adderess(self) -> net_rpc_pb2.ListenAddrResponse:
        req = net_rpc_pb2.ListenAddrRequest()
        return self.client.ListenAddr(req)

    def peers(self) -> net_rpc_pb2.PeersResponse:
        req = net_rpc_pb2.PeersRequest()
        return self.client.Peers(req)

    def find_peer(self, peer_id: str) -> net_rpc_pb2.FindPeerResponse:
        req = net_rpc_pb2.FindPeerRequest(peer_id=peer_id)
        return self.client.FindPeer(req)

    def connect_peer(
        self, peer_addr_info: net_rpc_pb2.PeerAddrInfo
    ) -> net_rpc_pb2.ConnectPeerResponse:
        req = net_rpc_pb2.ConnectPeerRequest(peer_info=peer_addr_info)
        return self.client.ConnectPeer(req)

    def disconnect_peer(self, peer_id: str) -> net_rpc_pb2.DisconnectPeerResponse:
        req = net_rpc_pb2.DisconnectPeerRequest(peer_id=peer_id)
        return self.client.DisconnectPeer(req)

    def connectedness(self, peer_id: str) -> net_rpc_pb2.ConnectPeerResponse:
        req = net_rpc_pb2.ConnectPeerRequest(peer_id=peer_id)
        return self.client.Connectedness(req)
