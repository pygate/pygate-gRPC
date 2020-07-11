import logging
import pytest

from proto.ffs_rpc_pb2 import CreateResponse, AddToHotRequest, AddrInfo
from pygate_grpc.client import PowerGateClient

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def ffs_instance(pygate_client: PowerGateClient):
    return pygate_client.ffs.create()


def test_grpc_ffs_create(pygate_client: PowerGateClient):
    res = pygate_client.ffs.create()

    assert type(res) == CreateResponse
    assert res.id is not None
    assert res.token is not None


def test_grpc_ffs_list_api(pygate_client: PowerGateClient, ffs_instance):
    res = pygate_client.ffs.list_api()

    assert res is not None
    assert ffs_instance.id in res.instances


def test_grpc_ffs_add_to_hot(pygate_client: PowerGateClient, ffs_instance):
    res = pygate_client.ffs.add_to_hot(test_chunks(), ffs_instance.token)

    assert res is not None
    assert res.cid is not None

def test_grpc_ffs_add_then_get_content(pygate_client: PowerGateClient, ffs_instance):
    res = pygate_client.ffs.add_to_hot(test_chunks(), ffs_instance.token)
    
    assert res is not None

    pygate_client.ffs.push(res.cid, ffs_instance.token)
    f = pygate_client.ffs.get(res.cid, ffs_instance.token)

    assert next(f) == b'test_content'

def test_grpc_ffs_list_wallet(pygate_client: PowerGateClient, ffs_instance):
    res = pygate_client.ffs.addrs_list(token=ffs_instance.token)

    assert res is not None
    assert len(res.addrs) == 1
    assert res.addrs[0].name == 'Initial Address'
    assert res.addrs[0].type == 'bls'

def test_create_new_wallet_address(pygate_client: PowerGateClient, ffs_instance: CreateResponse):
    new_addr_name = 'test'
    addr = pygate_client.ffs.addrs_new(name=new_addr_name, token=ffs_instance.token)

    assert addr is not None
    assert addr.addr is not None

    res = pygate_client.ffs.addrs_list(token=ffs_instance.token)

    assert res is not None
    assert len(res.addrs) == 2
    
    expected_addr = AddrInfo(name=new_addr_name, addr=addr.addr, type='bls')
    assert expected_addr in res.addrs
    
    
def test_chunks():
    for _ in range(1):
        yield AddToHotRequest(chunk=bytes('test_content', 'ASCII'))
