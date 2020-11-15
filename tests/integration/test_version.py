import logging

from pygate_grpc.client import PowerGateClient
from pygate_grpc.types import BuildInfo

logger = logging.getLogger(__name__)


def test_build_info(pygate_client: PowerGateClient):
    build_info = pygate_client.build_info()

    assert build_info is not None
    assert type(build_info) == BuildInfo


def test_get_user_id(pygate_client: PowerGateClient):
    user = pygate_client.admin.users.create()

    user_id = pygate_client.user_id(user.token)

    assert user_id == user.id
