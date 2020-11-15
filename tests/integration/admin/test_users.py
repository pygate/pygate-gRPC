import logging

import pytest

from pygate_grpc.client import PowerGateClient
from pygate_grpc.types import User

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def user(pygate_client: PowerGateClient):
    return pygate_client.admin.users.create()


def test_grpc_user_create(pygate_client: PowerGateClient):
    new_user = pygate_client.admin.users.create()

    assert type(new_user) == User
    assert new_user.id is not None
    assert new_user.token is not None


def test_grpc_user_list(pygate_client: PowerGateClient, user: User):
    users = pygate_client.admin.users.list()

    assert type(users) == list
    assert users is not None
    assert user in users
