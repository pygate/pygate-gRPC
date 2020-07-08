import pytest

from pygate_grpc import PowerGateClient

def pytest_configure(config):
    print("TEEST")

@pytest.fixture(scope="module")
def pygate_client():
    return PowerGateClient("127.0.0.1", 5002)

